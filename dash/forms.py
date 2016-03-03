from django import forms
from .models import MergeJob

class MergeForm(forms.ModelForm):
    class Meta:
        model = MergeJob
        fields = ('template_folder', 'template', 'flow', 'output_folder', 'ident','payload', 'payload_type', 'test_case', 'data_folder', 'data_file',)                
    