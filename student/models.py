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