from django.shortcuts import render, redirect
from Admin.models import Student, ProjectGroup

def student_dashboard(request):
    if 'student_id' not in request.session:
        return redirect('guest:guest_login')

    student = Student.objects.get(id=request.session['student_id'])

    try:
        group = ProjectGroup.objects.get(students=student)
    except ProjectGroup.DoesNotExist:
        group = None

    context = {
        'student': student,
        'group': group
    }

    return render(request, 'student/student_dashboard.html', context)


def student_logout(request):
    request.session.flush()
    return redirect('guest:guest_login')
