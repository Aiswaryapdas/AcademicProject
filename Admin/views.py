from django.shortcuts import render, redirect
from Admin.models import *

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
def student_register(request):
    if request.method == "POST":
        admission_number = request.POST.get('admission_number')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        course = request.POST.get('course')
        course_batch = request.POST.get('course_batch')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            Student.objects.create(
                admission_number=admission_number,
                name=name,
                email=email,
                phone=phone,
                department=department,
                course=course,
                course_batch=course_batch,
                password=password
            )
            return redirect('WAdmin:student_register')

    return render(request,'Admin/student_reg.html')

def admin_dashboard(request):
    # Optional: check admin session
    if 'admin_id' not in request.session:
        return redirect('guest:guest_login')

    faculty_count = tbl_faculty.objects.count()
    student_count = tbl_student.objects.count()

    context = {
        'faculty_count': faculty_count,
        'student_count': student_count
    }

    return render(request, 'Admin/admin_dashboard.html', context)