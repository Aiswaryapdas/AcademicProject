from django.db import models

class Faculty(models.Model):
    faculty_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.faculty_id} - {self.name}"

class Student(models.Model):
    admission_number = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    course_batch = models.CharField(max_length=20)  # e.g. 2024-2026
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.admission_number} - {self.name}"
    
    

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = "admin"   # VERY IMPORTANT

    def __str__(self):
        return self.username

