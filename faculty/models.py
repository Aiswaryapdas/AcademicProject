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

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from Admin.models import ReviewSchedule
from Admin.models import Student


class ReviewMark(models.Model):
    review = models.ForeignKey(ReviewSchedule, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    mark = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'student')

    def __str__(self):
        return f"{self.student} - {self.review} - {self.mark}"        