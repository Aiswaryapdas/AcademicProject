from django.shortcuts import render, redirect
from Admin.models import *
from .forms import ProjectGroupForm




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
    # Optional: check admin session
    if 'admin_id' not in request.session:
        return redirect('guest:guest_login')

    faculty_count = Faculty.objects.count()
    student_count = Student.objects.count()

    context = {
        'faculty_count': faculty_count,
        'student_count': student_count
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