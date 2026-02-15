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