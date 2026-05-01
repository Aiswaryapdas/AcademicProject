from django.db import models
from Admin.models import DocumentSchedule
from Admin.models import Student

class DocumentSubmission(models.Model):

    schedule = models.ForeignKey(DocumentSchedule, on_delete=models.CASCADE)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    file = models.FileField(upload_to='documents/')

    submitted_at = models.DateTimeField(auto_now_add=True)

    faculty_mark = models.IntegerField(null=True, blank=True)
    faculty_remark = models.TextField(null=True, blank=True)   


class ProjectProposal(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey('Admin.Student', on_delete=models.CASCADE)    
    title = models.CharField(max_length=200)
    domain = models.CharField(max_length=100)
    technology = models.CharField(max_length=200)
    description = models.TextField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    admin_remark = models.TextField(blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title    


from django.db import models

class Project(models.Model):
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)

    # Assuming you already have these models
    student = models.ForeignKey('Admin.Student', on_delete=models.CASCADE)
    faculty = models.ForeignKey('Admin.Faculty', on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey('Admin.ProjectGroup', on_delete=models.SET_NULL, null=True, blank=True)
    proposal = models.ForeignKey('student.ProjectProposal', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Approved')

    domain = models.CharField(max_length=100, blank=True, null=True)
    technology = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title        