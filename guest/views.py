
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from Admin.models import Admin, Student, Faculty


def login(request):
    if request.method == "POST":
        cemail = request.POST.get("txt_email")
        cpassword = request.POST.get("txt_pass")

        student_count = Student.objects.filter(email=cemail, password=cpassword).count()
        faculty_count = Faculty.objects.filter(email=cemail, password=cpassword).count()
        admin_count = Admin.objects.filter(email=cemail, password=cpassword).count()

        if student_count > 0:
            student_data = Student.objects.get(email=cemail, password=cpassword)
            request.session['student_id'] = student_data.id
            return redirect('student:homepage')

        elif faculty_count > 0:
            faculty_data = Faculty.objects.get(email=cemail, password=cpassword)
            request.session['faculty_id'] = faculty_data.id
            return redirect('faculty:homepage')

        elif admin_count > 0:
            admin_data = Admin.objects.get(email=cemail, password=cpassword)
            request.session['admin_id'] = admin_data.id
            return redirect('WAdmin:admin_dashboard')

        else:
            msg = "Invalid credentials!!"
            return render(request, 'Guest/Login.html', {'msg': msg})

    return render(request, 'Guest/Login.html')