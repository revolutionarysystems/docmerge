from django import forms
from .models import MergeJob, RefreshJob

class MergeForm(forms.ModelForm):
    class Meta:
        model = MergeJob
        fields = (
        	'template_folder', 'template_subfolder', 'template', 'flow', 'output_folder', 'identifier',
        	'payload', 'payload_type', 'test_case', 'data_folder', 'data_file', 'data_root',
        	'branding_folder', 'branding_file',
        	'xform_folder', 'xform_file',
        	)                

class TestNavForm(forms.ModelForm):
    class Meta:
        model = MergeJob
        fields = (
            'template_subfolder',
            )                

class SimpleMergeForm(forms.ModelForm):
    class Meta:
        model = MergeJob
        fields = (
            'template_subfolder',
            'template', 'flow',
            'data_file', 'data_root',
            'branding_file',
            'xform_file',
            )                
#        fields = (
#        	'template_subfolder', 'template', 'flow', 'identifier',
#        	'data_file', 'data_root',
#        	'branding_file',
#        	'xform_file',
#        	)                

class RefreshForm(forms.ModelForm):
    class Meta:
        model = RefreshJob
        fields = (
            'local', 'remote',
            )                

class UploadZipForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()
    