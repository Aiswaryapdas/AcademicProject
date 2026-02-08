
import os
import django
import sys

# Add project root to path
sys.path.append('d:/AcademicProject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AcademicProject.settings')
django.setup()

from Admin.models import Admin, Student, Faculty

print("Checking for collisions...")
email = 'admin@gmail.com'
password = 'admin123'

s_count = Student.objects.filter(email=email, password=password).count()
f_count = Faculty.objects.filter(email=email, password=password).count()
a_count = Admin.objects.filter(email=email, password=password).count()

print(f"Student count: {s_count}")
print(f"Faculty count: {f_count}")
print(f"Admin count: {a_count}")

if s_count > 0:
    print("LOGIN LOGIC WOULD LOG IN AS STUDENT!")
elif f_count > 0:
    print("LOGIN LOGIC WOULD LOG IN AS FACULTY!")
elif a_count > 0:
    print("LOGIN LOGIC WOULD LOG IN AS ADMIN!")
else:
    print("LOGIN LOGIC WOULD FAIL!")
