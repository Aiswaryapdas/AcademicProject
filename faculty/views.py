from django.shortcuts import render, redirect
from Admin.models import Faculty, ProjectGroup
from Admin.models import ReviewSchedule

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
        date = request.POST.get('attendance_date')
        if not date:
            # if no date selected, redirect back
            return redirect('/faculty/attendance/')

        # Save attendance for each student
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={'faculty_id': faculty_id, 'status': status}
                )
        return redirect('/faculty/dashboard/')  # back to dashboard after saving

    return render(request, 'faculty/attendance_mark.html', {'students': students})


def logout_view(request):
    request.session.flush()
    return redirect('guest:guest_login')
