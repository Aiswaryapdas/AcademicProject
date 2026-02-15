from django.shortcuts import render, redirect
from Admin.models import Faculty, ProjectGroup

def homepage(request):

    if 'faculty_id' not in request.session:
        return redirect('guest:guest_login')

    faculty = Faculty.objects.get(id=request.session['faculty_id'])

    # Get group assigned to this faculty
    group = ProjectGroup.objects.filter(faculty=faculty).first()

    students = []
    if group:
        students = group.students.all()

    return render(request, 'Faculty/faculty_dashboard.html', {
        'faculty': faculty,
        'group': group,
        'students': students
    })

def logout_view(request):
    request.session.flush()
    return redirect('guest:guest_login')
