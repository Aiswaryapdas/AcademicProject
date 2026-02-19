from django.shortcuts import render, redirect, get_object_or_404
from Admin.models import *
from .forms import ProjectGroupForm
from .models import ReviewSchedule
from .forms import ReviewScheduleForm
from .models import SubmissionSchedule
from django.utils import timezone
from Admin.models import DocumentSubmission





def faculty_register(request):
    if request.method == "POST":
        faculty_id = request.POST.get('faculty_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            Faculty.objects.create(
                faculty_id=faculty_id,
                name=name,
                email=email,
                phone=phone,
                department=department,
                designation=designation,
                password=password
            )
            return redirect('WAdmin:faculty_register')

    return render(request, 'Admin/faculty_reg.html')


from django.contrib import messages
from Admin.models import Student

def student_register(request):
    if request.method == "POST":
        admission_number = request.POST.get('admission_number')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        course = request.POST.get('course')
        academic_batch = request.POST.get('academic_batch')
        file_batch = request.POST.get('file_batch')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check for duplicates
        if Student.objects.filter(admission_number=admission_number).exists():
            messages.error(request, "Admission number already exists!")
        elif Student.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match!")
        else:
            Student.objects.create(
                admission_number=admission_number,
                name=name,
                email=email,
                phone=phone,
                department=department,
                course=course,
                academic_batch=academic_batch,
                file_batch=file_batch,
                password=password
            )
            messages.success(request, "Student registered successfully!")
            return redirect('WAdmin:student_register')

    return render(request, 'Admin/student_reg.html')



def admin_dashboard(request):

    faculty_count = Faculty.objects.count()
    student_count = Student.objects.count()
    project_group_count = ProjectGroup.objects.count()

   

    context = {
        'faculty_count': faculty_count,
        'student_count': student_count,
        'project_group_count': project_group_count,
        
    }

    return render(request, 'Admin/admin_dashboard.html', context)



def faculty_list(request):
    # Optional: Check if admin is logged in
    if 'admin_id' not in request.session:
        return redirect('guest:guest_login')

    faculties = Faculty.objects.all()  # Get all faculty objects
    context = {
        'faculties': faculties
    }
    return render(request, 'Admin/faculty_list.html', context)
from Admin.models import Student

def student_list(request):
    # Optional: Check if admin is logged in
    if 'admin_id' not in request.session:
        return redirect('guest:guest_login')

    students = Student.objects.all()  # Get all student objects
    context = {
        'students': students
    }
    return render(request, 'Admin/student_list.html', context)

def create_project_group(request):
    if request.method == 'POST':
        form = ProjectGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('WAdmin:admin_dashboard')
    else:
        form = ProjectGroupForm()

    return render(request, 'Admin/assign_group.html', {'form': form})

def review_schedule(request):
    reviews = ReviewSchedule.objects.all().order_by('review_date', 'review_time')
    context = {'reviews': reviews}
    return render(request, 'Admin/review_schedule.html', context)

def review_schedule_add(request):
    if request.method == 'POST':
        form = ReviewScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('WAdmin:review_schedule')
    else:
        form = ReviewScheduleForm()
    return render(request, 'Admin/review_schedule_add.html', {'form': form})

def review_schedule_edit(request, id):
    schedule = get_object_or_404(ReviewSchedule, id=id)

    if request.method == 'POST':
        form = ReviewScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('WAdmin:review_schedule')
    else:
        form = ReviewScheduleForm(instance=schedule)

    return render(request, 'Admin/review_schedule_add.html', {'form': form})

def review_schedule_delete(request, id):
    schedule = get_object_or_404(ReviewSchedule, id=id)
    schedule.delete()
    return redirect('WAdmin:review_schedule')

def view_project_groups(request):
    groups = ProjectGroup.objects.all()
    return render(request, 'Admin/view_project_group.html', {'groups': groups})

def faculty_review_schedule(request):
    if 'faculty_id' not in request.session:
        return redirect('guest:guest_login')

    reviews = ReviewSchedule.objects.all().order_by('review_date', 'review_time')
    context = {'reviews': reviews}
    return render(request, 'Admin/faculty_review_schedule.html', context)


# Student view
def student_review_schedule(request):
    if 'student_id' not in request.session:
        return redirect('guest:guest_login')

    reviews = ReviewSchedule.objects.all().order_by('review_date', 'review_time')
    context = {'reviews': reviews}
    return render(request, 'Admin/student_review_schedule.html', context)

def admin_view_submissions(request):
    submissions = DocumentSubmission.objects.all()
    return render(request, 'Admin/view_all_submissions.html', {
        'submissions': submissions
    })

from django.shortcuts import get_object_or_404

# ===============================
# DOCUMENT SCHEDULE (ADMIN)
# ===============================

# LIST PAGE
def document_schedule(request):
    schedules = SubmissionSchedule.objects.all().order_by('-created_at')
    now = timezone.now()

    for schedule in schedules:
        if schedule.start_datetime > now:
            schedule.status = "Upcoming"
        elif schedule.end_datetime < now:
            schedule.status = "Expired"
        else:
            schedule.status = "Active"

    return render(request, 'Admin/document_submission.html', {
        'schedules': schedules
    })


# ADD PAGE
def document_schedule_add(request):
    if request.method == 'POST':
        SubmissionSchedule.objects.create(
            title=request.POST.get('title'),
            document_type=request.POST.get('document_type'),
            description=request.POST.get('description'),
            start_datetime=request.POST.get('start_datetime'),
            end_datetime=request.POST.get('end_datetime'),
            allowed_file_type=request.POST.get('allowed_file_type'),
            max_file_size=request.POST.get('max_file_size'),
           
        )
        return redirect('WAdmin:document_schedule')

    return render(request, 'Admin/document_schedule_add.html')


# EDIT
def document_schedule_edit(request, id):
    schedule = get_object_or_404(SubmissionSchedule, id=id)

    if request.method == 'POST':
        schedule.title = request.POST.get('title')
        schedule.document_type = request.POST.get('document_type')
        schedule.description = request.POST.get('description')
        schedule.start_datetime = request.POST.get('start_datetime')
        schedule.end_datetime = request.POST.get('end_datetime')
        schedule.allowed_file_type = request.POST.get('allowed_file_type')
        schedule.max_file_size = request.POST.get('max_file_size')
        schedule.max_attempts = request.POST.get('max_attempts')
        schedule.save()
        return redirect('WAdmin:document_schedule')

    return render(request, 'Admin/document_schedule_add.html', {
        'schedule': schedule
    })


# DELETE
def document_schedule_delete(request, id):
    schedule = get_object_or_404(SubmissionSchedule, id=id)
    schedule.delete()
    return redirect('WAdmin:document_schedule')


def all_submissions(request):
    submissions = DocumentSubmission.objects.select_related(
        'student', 'schedule'
    )

    return render(request, 'Admin/all_submissions.html', {
        'submissions': submissions
    })

from datetime import datetime
from calendar import monthrange
from django.shortcuts import render
from Admin.models import Student
from faculty.models import Attendance

def admin_attendance(request):
    if 'admin_id' not in request.session:
        return redirect('guest:guest_login')

    today = datetime.today()
    year = today.year
    month = today.month

    days_in_month = monthrange(year, month)[1]
    days_range = range(1, days_in_month + 1)

    students = Student.objects.all()

    attendance_data = []

    for student in students:
        records = Attendance.objects.filter(
            student=student,
            date__year=year,
            date__month=month
        )

        attendance_display = []

        present_count = records.filter(status="Present").count()
        absent_count = records.filter(status="Absent").count()

        for day in days_range:
            record = records.filter(date__day=day).first()

            if record:
                if record.status == "Present":
                    attendance_display.append(("P", "present"))
                else:
                    attendance_display.append(("A", "absent"))
            else:
                attendance_display.append(("-", "empty"))

        attendance_data.append({
            "student_id": student.id,
            "name": student.name,
            "present": present_count,
            "absent": absent_count,
            "attendance_display": attendance_display
        })

    return render(request, "Admin/admin_attendance.html", {
        "attendance_data": attendance_data,
        "days_range": days_range,
        "month": today.strftime("%B"),
        "year": year,
    })