from django import forms
from .models import MergeJob

class MergeForm(forms.ModelForm):
    class Meta:
        model = MergeJob
        fields = ('template_folder', 'template', 'flow', 'output_folder', 'ident',)                



    