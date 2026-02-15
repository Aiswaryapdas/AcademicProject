from django import forms
from .models import ProjectGroup, Faculty, Student


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
