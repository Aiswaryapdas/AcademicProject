from django.shortcuts import render, redirect
from Admin.models import Faculty, ProjectGroup
from Admin.models import ReviewSchedule
from .models import ReviewMark
from django.apps import apps
from .models import Attendance


def homepage(request):

    if 'faculty_id' not in request.session:
        return redirect('guest:guest_login')

    faculty = Faculty.objects.get(id=request.session['faculty_id'])

    # Get group assigned to this faculty
    group = ProjectGroup.objects.filter(faculty=faculty).first()

    students = []
    if group:
        students = group.students.all()

    reviews = ReviewSchedule.objects.all().order_by('review_date', 'review_time')

    return render(request, 'Faculty/faculty_dashboard.html', {
        'faculty': faculty,
        'group': group,
        'students': students,
        'reviews': reviews 

    })


def faculty_view_submissions(request):
    faculty = Faculty.objects.get(id=request.session['faculty_id'])
    group = ProjectGroup.objects.filter(faculty=faculty).first()

    submissions = DocumentSubmission.objects.filter(
        student__in=group.students.all()
    )

    return render(request, 'Faculty/view_submissions.html', {
        'submissions': submissions
    })

def faculty_view_submissions(request, schedule_id):
    schedule = get_object_or_404(SubmissionSchedule, id=schedule_id)

    faculty = request.user.faculty

    submissions = DocumentSubmission.objects.filter(
        schedule=schedule,
        student__project_group__faculty=faculty
    )

    return render(request, 'Faculty/view_submissions.html', {
        'submissions': submissions,
        'schedule': schedule
    })

def add_mark(request, submission_id):
    submission = get_object_or_404(DocumentSubmission, id=submission_id)

    if request.method == "POST":
        submission.mark = request.POST.get('mark')
        submission.save()

    return redirect('faculty:view_submissions', submission.schedule.id)

from datetime import date
from django.shortcuts import redirect, render
from django.contrib import messages  # if you want to show error messages
from django.apps import apps
from faculty.models import Attendance

def attendance_mark(request):
    # Check custom faculty login session
    if 'faculty_id' not in request.session:
        return redirect('/faculty/login/')  # your faculty login page

    faculty_id = request.session['faculty_id']
    faculty_name = request.session.get('faculty_name')

    # Load ProjectGroup model and Student model
    Student = apps.get_model('Admin', 'Student')  # replace 'Admin' with your app name
    ProjectGroup = apps.get_model('Admin', 'ProjectGroup')

    # Get the project group for this faculty
    group = ProjectGroup.objects.filter(faculty_id=faculty_id).first()
    students = Student.objects.filter(projectgroup=group) if group else []

    if request.method == 'POST':
        selected_date = request.POST.get("selected_date")
        if not selected_date:
            return redirect('/faculty/attendance/')

        today_date = date.today().isoformat()

        # Prevent past dates
        if selected_date < date.today():
            messages.error(request, "You cannot mark attendance for past dates.")
            return redirect('/faculty/attendance/')

        # Save attendance for each student
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    today_date=today_date,  # use the selected_date
                    defaults={'faculty_id': faculty_id, 'status': status}
                )
        return redirect('/faculty/dashboard/')  # back to dashboard after saving

    # Pass today's date to template for min date restriction in HTML
    today_date = date.today()
    return render(request, 'faculty/attendance_mark.html', {
        'students': students,
        'today_date': today_date
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from Admin.models import ReviewSchedule, ProjectGroup, Student
from .models import ReviewMark


def add_review_marks(request, review_id):

    review = get_object_or_404(ReviewSchedule, id=review_id)

    faculty_id = request.session.get('faculty_id')

    # get faculty group
    group = ProjectGroup.objects.get(faculty_id=faculty_id)

    # students in that group
    students = Student.objects.filter(projectgroup=group)

    # existing marks
    marks = ReviewMark.objects.filter(review=review)

    mark_dict = {m.student_id: m.mark for m in marks}

    # calculate total marks of each student
    totals = ReviewMark.objects.values('student').annotate(total=Sum('mark'))

    total_dict = {t['student']: t['total'] for t in totals}

    if request.method == "POST":

        for student in students:

            mark = request.POST.get(f"mark_{student.id}")

            if mark:
                ReviewMark.objects.update_or_create(
                    review=review,
                    student=student,
                    defaults={'mark': mark}
                )

        return redirect('faculty:homepage')

    context = {
        'review': review,
        'students': students,
        'mark_dict': mark_dict,
        'total_dict': total_dict
    }

    return render(request, 'Faculty/add_review_marks.html', context)
def logout_view(request):
    request.session.flush()
    return redirect('guest:guest_login')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Admin.models import Student
from Admin.models import DocumentSchedule
from student.models import DocumentSubmission

def faculty_document_view(request):
    students = Student.objects.all()  # all students (or filter by assigned faculty if needed)
    schedules = DocumentSchedule.objects.all()

    # Handle marks submission
    if request.method == 'POST':
        for student in students:
            for i, schedule in enumerate(schedules):
                mark_key = f'mark_{student.id}_{i}'
                mark_value = request.POST.get(mark_key)
                if mark_value:
                    submission, created = DocumentSubmission.objects.get_or_create(
                        student=student,
                        document_schedule=schedule
                    )
                    submission.faculty_mark = float(mark_value)
                    submission.save()
        return redirect('faculty:faculty_document_view')

    # Prepare submissions data
    submissions_list = []
    for student in students:
        for schedule in schedules:
            
            submission_qs = DocumentSubmission.objects.filter(
            student=student,
            schedule=schedule
        ).order_by('-submitted_at')  # latest submission first
        if submission_qs.exists():
                submission = submission_qs.first() 
                submissions_list.append({
                    'student': student,
                    'schedule': schedule,
                    'submitted': True,
                    'file': submission.uploaded_file,
                    'submitted_at': submission.uploaded_at,
                    'mark': submission.faculty_mark
                })
        else:
             submissions_list.append({
                    'student': student,
                    'schedule': schedule,
                    'submitted': False,
                    'file': None,
                    'submitted_at': None,
                    'mark': None
                })

    return render(request, 'faculty/document_list.html', {'submissions': submissions_list})


def document_schedule_list(request):

    schedules = DocumentSchedule.objects.all()

    return render(request,'faculty/document_schedules.html',{
        'schedules': schedules
    })

def schedule_submissions(request, schedule_id):

    schedule = get_object_or_404(DocumentSchedule, id=schedule_id)

    # get faculty id from session
    faculty_id = request.session.get('faculty_id')

    # get faculty group
    group = ProjectGroup.objects.filter(faculty_id=faculty_id).first()

    # get only students in that group
    students = Student.objects.filter(projectgroup=group)

    # SAVE MARK + REMARK
    if request.method == "POST":

        for student in students:

            submission = DocumentSubmission.objects.filter(
                student=student,
                schedule=schedule
            ).first()

            if submission:

                mark = request.POST.get(f"mark_{student.id}")
                remark = request.POST.get(f"remark_{student.id}")

                if mark:
                    submission.faculty_mark = mark

                submission.faculty_remark = remark
                submission.save()

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

    return render(request, 'Faculty/schedule_submissions.html', {
        'schedule': schedule,
        'data': data
    })