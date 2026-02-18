from django import forms
from .models import ProjectGroup, Faculty, Student, ReviewSchedule

class ProjectGroupForm(forms.ModelForm):
    class Meta:
        model = ProjectGroup
        fields = ['group_name', 'faculty', 'students']
        widgets = {
            'group_name': forms.TextInput(attrs={'class': 'form-control'}),
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'students': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get assigned faculty IDs
        assigned_faculty = ProjectGroup.objects.values_list('faculty_id', flat=True)

        # Get assigned student IDs
        assigned_students = ProjectGroup.objects.values_list('students__id', flat=True)

        # Filter directly (no if condition)
        self.fields['faculty'].queryset = Faculty.objects.exclude(id__in=assigned_faculty)
        self.fields['students'].queryset = Student.objects.exclude(id__in=assigned_students)

class ReviewScheduleForm(forms.ModelForm):
    class Meta:
        model = ReviewSchedule
        fields = '__all__'
        widgets = {
            'review_topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter review topic'}),
            'review_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'review_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'review_status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional remarks'}),
        }
