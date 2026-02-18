from django.shortcuts import render, redirect
from Admin.models import Faculty, ProjectGroup
from Admin.models import ReviewSchedule



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



def logout_view(request):
    request.session.flush()
    return redirect('guest:guest_login')
