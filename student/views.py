from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from Admin.models import Student, ProjectGroup, ReviewSchedule, SubmissionSchedule,DocumentSubmission
from faculty.models import Attendance
from datetime import datetime
from calendar import monthrange

def student_dashboard(request):
    student = Student.objects.get(id=request.session['student_id'])

    # Project group
    group = ProjectGroup.objects.filter(students=student).first()

    # Reviews (simple for now)
    reviews = ReviewSchedule.objects.all()

    now = timezone.now()

    schedules = SubmissionSchedule.objects.all()

    for schedule in schedules:
        # ---- STATUS CALCULATION ----
        if now < schedule.start_datetime:
            schedule.status = "Upcoming"
        elif schedule.start_datetime <= now <= schedule.end_datetime:
            schedule.status = "Active"
        else:
            schedule.status = "Expired"

        # ---- CHECK SUBMISSION ----
        submission = DocumentSubmission.objects.filter(
            student=student,
            schedule=schedule
        ).first()

        schedule.submission = submission

    context = {
        'student': student,
        'group': group,
        'reviews': reviews,
        'schedules': schedules,
    }

    return render(request, 'student/student_dashboard.html', context)

def student_logout(request):
    request.session.flush()
    return redirect('guest:guest_login')



def student_document_schedules(request):
    schedules = SubmissionSchedule.objects.all()
    now = timezone.now()
    student = request.user.student

    for schedule in schedules:

        # Check status
        if schedule.start_datetime > now:
            schedule.status = "Upcoming"
        elif schedule.end_datetime < now:
            schedule.status = "Expired"
        else:
            schedule.status = "Active"

        # Get student's submission
        schedule.submission = DocumentSubmission.objects.filter(
            student=student,
            schedule=schedule
        ).first()

    return render(request, 'Student/student_document_schedules.html', {
        'schedules': schedules
    })

def upload_document(request, id):
    schedule = get_object_or_404(SubmissionSchedule, id=id)
    student = request.user.student
    now = timezone.now()

    # 🔒 1. Check if submission not started yet
    if now < schedule.start_datetime:
        messages.warning(request, "Submission has not started yet.")
        return redirect('student:student_document_schedules')

    # 🔒 2. Check if deadline passed
    if now > schedule.end_datetime:
        messages.error(request, "Deadline has passed. You cannot upload.")
        return redirect('student:student_document_schedules')

    # 🔒 3. Prevent multiple submissions (if only 1 allowed)
    already_submitted = DocumentSubmission.objects.filter(
        student=student,
        schedule=schedule
    ).exists()

    if already_submitted:
        messages.warning(request, "You have already submitted this document.")
        return redirect('student:student_document_schedules')

    # ✅ 4. Handle file upload
    if request.method == "POST":
        file = request.FILES.get('file')

        if not file:
            messages.error(request, "Please select a file.")
            return redirect('student:upload_document', id=id)

        DocumentSubmission.objects.create(
            student=student,
            schedule=schedule,
            file=file
        )

        messages.success(request, "Document uploaded successfully!")
        return redirect('student:student_document_schedules')

    return render(request, 'Student/upload_document.html', {
        'schedule': schedule
    })



def student_attendance(request):
    if 'student_id' not in request.session:
        return redirect('guest:guest_login')

    student = Student.objects.get(id=request.session['student_id'])

    today = datetime.today()
    year = today.year
    month = today.month

    records = Attendance.objects.filter(
        student=student,
        date__year=year,
        date__month=month
    ).order_by('date')

    # Count attendance
    total_days = records.count()
    present_days = records.filter(status="Present").count()

    total_periods = total_days * 5
    present_periods = present_days * 5

    percentage = 0
    if total_periods > 0:
        percentage = round((present_periods / total_periods) * 100, 2)

    # Days in current month
    days_in_month = monthrange(year, month)[1]
    days_range = range(1, days_in_month + 1)
    periods = range(1, 6)  # 5 periods

    # Create clean display structure (NO template logic needed)
    attendance_display = {}

    for period in periods:
        attendance_display[period] = []

        for day in days_range:
            record = records.filter(date__day=day).first()

            if record:
                if record.status == "Present":
                    attendance_display[period].append(("P", "present"))
                else:
                    attendance_display[period].append(("A", "absent"))
            else:
                attendance_display[period].append(("-", "empty"))

    return render(request, 'student/attendance.html', {
        'student': student,
        'days_range': days_range,
        'attendance_display': attendance_display,
        'percentage': percentage,
        'month': today.strftime("%B"),
        'year': year,
    })
