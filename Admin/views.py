from django.shortcuts import render, redirect, get_object_or_404
from Admin.models import *
from .forms import ProjectGroupForm
from .models import ReviewSchedule
from .forms import ReviewScheduleForm

from django.utils import timezone

from django.utils.dateparse import parse_datetime




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
            messages.success(request, "Faculty Registered Successfully ✅")

            return redirect('WAdmin:faculty_register')   # ✅ redirect once ONLY

        else:
            messages.error(request, "Passwords do not match ❌")

            return redirect('WAdmin:faculty_register')   # ✅ redirect once ONLY

    return render(request, 'Admin/faculty_reg.html')

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
    faculties = Faculty.objects.all()
    return render(request, 'Admin/faculty_list.html', {'faculties': faculties})


def student_list(request):

    query = request.GET.get('q')

    if query:
        students = Student.objects.filter(
            name__icontains=query
        ) | Student.objects.filter(
            admission_number__icontains=query
        )
    else:
        students = Student.objects.all()

    return render(request, 'Admin/student_list.html', {'students': students})

def project_group_list(request):

    faculty_id = request.GET.get('faculty')

    if faculty_id:
        groups = ProjectGroup.objects.filter(faculty_id=faculty_id)
    else:
        groups = ProjectGroup.objects.all()

    faculties = Faculty.objects.all()

    return render(request, 'Admin/project_group_list.html',
                  {'groups': groups, 'faculties': faculties})

def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect('WAdmin:student_list')    

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

from django.shortcuts import render
from Admin.models import Student, ReviewSchedule
from faculty.models import ReviewMark

def admin_view_review_marks(request):

    students = Student.objects.all()
    reviews = ReviewSchedule.objects.all().order_by('review_date')

    table_data = []

    for student in students:

        marks = ReviewMark.objects.filter(student=student)

        review_marks = {}
        total = 0

        for mark in marks:
            review_marks[mark.review.id] = mark.mark
            total += mark.mark

        table_data.append({
            "student": student,
            "marks": review_marks,
            "total": total
        })

    context = {
        "students": table_data,
        "reviews": reviews
    }

    return render(request,"Admin/view_review_marks.html",context)




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
from datetime import date
from calendar import monthrange
from faculty.models import Attendance
from Admin.models import Student
from django.shortcuts import render

def semester_attendance_view(request):
    students = Student.objects.all()
    year = 2026
    semester_months = [1, 2, 3, 4]  # Jan-Apr

    # Month filter from GET (format YYYY-MM)
    month_filter = request.GET.get('month')
    if month_filter:
        filter_year, filter_month = map(int, month_filter.split('-'))
        months_to_show = [filter_month] if filter_year == year else []
    else:
        months_to_show = semester_months  # show all months

    # Prepare data month by month
    semester_data = []

    for month in months_to_show:
        month_last_day = monthrange(year, month)[1]
        days_range = [date(year, month, day) for day in range(1, month_last_day + 1)]

        month_data = []
        for student in students:
            student_record = {
                'student_id': student.id,
                'name': student.name,
                'present': 0,
                'absent': 0,
                'attendance_display': []
            }

            for day in days_range:
                att = Attendance.objects.filter(student=student, date=day).first()
                if att:
                    if att.status == 'Present':
                        student_record['present'] += 1
                        student_record['attendance_display'].append(('P', 'present'))
                    else:
                        student_record['absent'] += 1
                        student_record['attendance_display'].append(('A', 'absent'))
                else:
                    student_record['attendance_display'].append(('', 'empty'))

            month_data.append(student_record)

        semester_data.append({
            'month_name': date(year, month, 1).strftime('%B'),
            'days_range': days_range,
            'month_data': month_data
        })

    return render(request, 'Admin/semester_attendance.html', {
        'semester_data': semester_data,
        'year': year,
        'month_filter': month_filter
    })

from .models import DocumentSchedule
from django.shortcuts import render, redirect

def add_document_schedule(request):

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        file_format = request.POST.get("file_format")
        max_size = request.POST.get("max_size")

        DocumentSchedule.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            file_format=file_format,
            max_size=max_size
        )

        return redirect('WAdmin:document_schedule_list')

    return render(request,'Admin/add_document_schedule.html')

def document_schedule_list(request):

    schedules = DocumentSchedule.objects.all()

    return render(request,'Admin/document_schedule_list.html', {'schedules': schedules})

def edit_document_schedule(request, id):

    schedule = DocumentSchedule.objects.get(id=id)

    if request.method == "POST":

        schedule.title = request.POST.get("title")
        schedule.description = request.POST.get("description")
        schedule.start_date = request.POST.get("start_date")
        schedule.end_date = request.POST.get("end_date")
        schedule.file_format = request.POST.get("file_format")
        schedule.max_size = request.POST.get("max_size")

        schedule.save()

        return redirect('WAdmin:document_schedule_list')

    return render(request,'Admin/edit_document_schedule.html',{'schedule':schedule})

def delete_document_schedule(request, id):

    schedule = DocumentSchedule.objects.get(id=id)

    schedule.delete()

    return redirect('WAdmin:document_schedule_list')

from student.models import DocumentSubmission

def admin_view_document_submissions(request):

    schedules = DocumentSchedule.objects.all()
    students = Student.objects.all()

    data = []

    for schedule in schedules:
        for student in students:

            submission = DocumentSubmission.objects.filter(
                student=student,
                schedule=schedule
            ).first()

            data.append({
                'student': student,
                'schedule': schedule,
                'submission': submission
            })

    return render(request,'Admin/view_document_submissions.html',{
        'data': data
    })

def admin_document_schedules(request):

    schedules = DocumentSchedule.objects.all()

    return render(request,'Admin/document_schedules.html',{
        'schedules': schedules
    })

def admin_schedule_submissions(request, schedule_id):

    schedule = get_object_or_404(DocumentSchedule, id=schedule_id)

    students = Student.objects.all()

    data = []

    for student in students:

        submission = DocumentSubmission.objects.filter(
            student=student,
            schedule=schedule
        ).first()

        data.append({
            'student': student,
            'submission': submission
        })

    return render(request, 'Admin/schedule_submissions.html', {
        'schedule': schedule,
        'data': data
    })

from django.contrib.auth import logout

def admin_logout(request):
    """
    Logs out the currently logged-in admin and redirects to the login page.
    """
    logout(request)  # Clears the session
    return redirect('guest:guest_login')