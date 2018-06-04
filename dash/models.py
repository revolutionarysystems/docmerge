from django.db import models
from merge.resource_utils import local_folder_files as folder_files
from django.contrib.auth.models import User

class MergeJob(models.Model):

    template_folder = models.CharField(max_length=100)
    template_subfolder = models.CharField(max_length=100, choices=[("--","--")])
    template = models.CharField(max_length=100, choices=[("--","--")])
    flow = models.CharField(max_length=100, choices=[("--","--")])
    output_folder = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100)
    payload = models.TextField()
    payload_type = models.CharField(max_length=100)
    test_case = models.CharField(max_length=100)
    data_folder = models.CharField(max_length=100)
    data_file = models.CharField(max_length=100, choices=[("--","--")])
    data_root = models.CharField(max_length=100)
    branding_folder = models.CharField(max_length=100)
    branding_file = models.CharField(max_length=100, choices=[("--","--")])
    xform_folder = models.CharField(max_length=100)
    xform_file = models.CharField(max_length=100, choices=[("--","--"),("None","None")])

class RefreshJob(models.Model):

    local = models.CharField(max_length=100)
    remote = models.CharField(max_length=100)


class EditFile(models.Model):
    file_folder = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100, blank=True, null=True)
    file_content = models.TextField(max_length=1000, blank=True, null=True)

class ComposeTemplate(EditFile):
    template_subfolder = models.CharField(max_length=100, choices=[("--","--")])
    template_files = models.CharField(max_length=100, blank=True, null=True, choices=[("--","--")])
    template_test_case = models.CharField(max_length=100, blank=True, null=True, choices=[("--","--")])
    test_case_xform = models.CharField(max_length=100, blank=True, null=True, choices=[("--","--")])
    template_stylesheet = models.CharField(max_length=100, blank=True, null=True, choices=[("--","--")])
    template_stylesheet_content = models.TextField(max_length=1000, blank=True, null=True)
    #template_sample = models.TextField(max_length=1000)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    company = models.CharField(max_length=50, blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

