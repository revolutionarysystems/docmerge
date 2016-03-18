from django import forms
from .models import MergeJob

class MergeForm(forms.ModelForm):
    class Meta:
        model = MergeJob
        fields = (
        	'template_folder', 'template', 'flow', 'output_folder', 'identifier',
        	'payload', 'payload_type', 'test_case', 'data_folder', 'data_file', 'data_root',
        	'branding_folder', 'branding_file',
        	)                

class SimpleMergeForm(forms.ModelForm):
    class Meta:
        model = MergeJob
        fields = (
        	'template', 'flow', 'identifier',
        	'data_file', 'data_root',
        	'branding_file',
        	)                
    