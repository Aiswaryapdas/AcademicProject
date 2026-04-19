from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from Admin.models import Student, ProjectGroup, ReviewSchedule
from faculty.models import Attendance
from datetime import datetime
from calendar import monthrange

def student_dashboard(request):
    if 'student_id' not in request.session:
        return redirect('guest:guest_login')

    student = Student.objects.get(id=request.session['student_id'])

    # Project group
    group = ProjectGroup.objects.filter(students=student).first()

    # Reviews
    reviews = ReviewSchedule.objects.all()

    # Submission schedules
    schedules = DocumentSchedule.objects.all()

    for schedule in schedules:
        schedule.submission = DocumentSubmission.objects.filter(
            student=student,
            schedule=schedule
        ).first()

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

from django.shortcuts import render, redirect
from django.db.models import Sum
from faculty.models import ReviewMark


def view_my_marks(request):

    if 'student_id' not in request.session:
        return redirect('guest:guest_login')

    student_id = request.session.get('student_id')

    # get all marks of that student
    marks = ReviewMark.objects.filter(student_id=student_id).select_related('review')

    # calculate total
    total = ReviewMark.objects.filter(student_id=student_id).aggregate(total=Sum('mark'))

    context = {
        'marks': marks,
        'total': total['total']
    }

    return render(request, 'Student/view_marks.html', context)

def student_document_list(request):

    schedules = DocumentSchedule.objects.all()

    return render(request,'Student/student_document_list.html',{'schedules':schedules})

from django.shortcuts import render,redirect
from Admin.models import DocumentSchedule
from .models import DocumentSubmission
from django.utils import timezone


def student_document_list(request):

    student_id = request.session['student_id']

    schedules = DocumentSchedule.objects.all()

    today = timezone.now().date()

    data = []

    for s in schedules:

        submission = DocumentSubmission.objects.filter(
            schedule=s,
            student_id=student_id
        ).first()

        if today < s.start_date:
            status = "Not Started"
            allow_upload = False

        elif s.start_date <= today <= s.end_date:
            status = "Open"
            allow_upload = True

        else:
            status = "Closed"
            allow_upload = False

        data.append({
            "schedule": s,
            "submission": submission,
            "status": status,
            "allow_upload": allow_upload
        })

    return render(request,'student/student_document_list.html',{"data":data})

def upload_document(request, id):

    schedule = DocumentSchedule.objects.get(id=id)
    student_id = request.session['student_id']

    submission = DocumentSubmission.objects.filter(
        schedule=schedule,
        student_id=student_id
    ).first()

    if request.method == "POST":

        file = request.FILES.get('file')

        if submission:
            submission.file = file
            submission.save()
        else:
            DocumentSubmission.objects.create(
                schedule=schedule,
                student_id=student_id,
                file=file
            )

        return redirect('student:student_document_list')

    return render(request, 'student/upload_document.html', {
        'schedule': schedule,
        'submission': submission
    })

def student_document_marks(request):

    student_id = request.session.get('student_id')   # your login session

    submissions = DocumentSubmission.objects.filter(student_id=student_id)

    return render(request,'Student/document_marks.html',{
        'submissions': submissions
    })

from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from django.http import HttpResponse

def student_change_password(request):
    if request.method == 'POST':
        current = request.POST['current_password']
        new = request.POST['new_password']
        confirm = request.POST['confirm_password']

        user = request.session.get('student_id')

        from .models import Student
        student = Student.objects.get(id=user)

        # Check current password
        if current != student.password:
            return HttpResponse("""
                <script>
                    alert('Current password is incorrect');
                    window.history.back();
                </script>
            """)

        # Check new password match
        if new != confirm:
            return HttpResponse("""
                <script>
                    alert('New passwords do not match');
                    window.history.back();
                </script>
            """)

        # Update password
        student.password = new
        student.save()

        return HttpResponse("""
       <script>
            alert('Password changed successfully');
            window.location.href = "{path('dashboard/', views.student_dashboard, name='dashboard'),}";
        </script>
""")

    return render(request, 'student/student_change_password.html')


def student_profile(request):
    student_id = request.session.get('student_id')  # get logged-in student

    if student_id:
        student = Student.objects.get(id=student_id)
        return render(request, 'student/profile.html', {'student': student})
    else:
        return redirect('login') 