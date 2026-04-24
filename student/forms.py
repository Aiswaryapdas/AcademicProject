from django import forms
from .models import ProjectProposal

class ProjectProposalForm(forms.ModelForm):
    class Meta:
        model = ProjectProposal
        fields = ['title', 'domain', 'technology', 'description']