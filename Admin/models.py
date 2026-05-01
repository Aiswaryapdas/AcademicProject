from django.db import models
from django.utils import timezone

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
    course = models.CharField(max_length=10)  # BCA / MCA
    academic_batch = models.CharField(max_length=20)  # previously course_batch
    file_batch = models.CharField(max_length=5)  # A/B/C/D
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "admin"   # VERY IMPORTANT

    def __str__(self):
        return self.username

class ProjectGroup(models.Model):
    group_name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.group_name


# models.py
class ReviewSchedule(models.Model):
    review_date = models.DateField()
    review_time = models.TimeField()
    review_topic = models.CharField(max_length=200)
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    review_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    remarks = models.TextField(blank=True, null=True)  # optional notes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.review_topic} on {self.review_date} at {self.review_time}"
    
  
class DocumentSchedule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    file_format = models.CharField(max_length=50)
    max_size = models.IntegerField()  # size in MB
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title       


from django.db import models
from django.contrib.auth.models import User

class Notice(models.Model):
    TARGET_CHOICES = (
        ('ALL', 'All'),
        ('STUDENT', 'Student'),
        ('FACULTY', 'Faculty'),
    )

    title = models.CharField(max_length=200)
    message = models.TextField()
    target = models.CharField(max_length=10, choices=TARGET_CHOICES, default='ALL')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title