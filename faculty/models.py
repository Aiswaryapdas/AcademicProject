from django.db import models

class Attendance(models.Model):
    student = models.ForeignKey(
        'Admin.Student',  # <-- Correct app_label.ModelName
        on_delete=models.CASCADE
    )
    faculty_id = models.IntegerField()  # store faculty session id
    date = models.DateField()
    status = models.CharField(max_length=10)  # Present / Absent

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"