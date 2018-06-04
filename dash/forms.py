from django import forms
from .models import MergeJob, RefreshJob, ComposeTemplate

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

class EditFileForm(forms.ModelForm):
    class Meta:
        model = ComposeTemplate
        fields = (
            'file_name',
            'file_content',
            'file_folder',
            )                

class ComposeTemplateForm(forms.ModelForm):
    class Meta:
        model = ComposeTemplate
        fields = (
            'file_name',
            'file_content',
            'file_folder',
            'template_files',
            'template_subfolder',
            'template_test_case',
            'test_case_xform',
            'template_stylesheet',
            'template_stylesheet_content',
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
    file = forms.FileField(label="Select a backup .zip file to load")
    clear = forms.BooleanField(required=False, label="Clear existing resources?")
    