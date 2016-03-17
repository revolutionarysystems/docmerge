from django.db import models
from merge.merge_utils import folder_files

class MergeJob(models.Model):

    template_folder = models.CharField(max_length=100)
    template = models.CharField(max_length=100, choices=[(file["name"],file["name"]) for file in folder_files("/Doc Merge/Templates")])
    flow = models.CharField(max_length=100)
    output_folder = models.CharField(max_length=100)
    ident = models.CharField(max_length=100)
    payload = models.TextField()
    payload_type = models.CharField(max_length=100)
    test_case = models.CharField(max_length=100)
    data_folder = models.CharField(max_length=100)
    data_file = models.CharField(max_length=100, choices=[(file["name"],file["name"]) for file in folder_files("/Doc Merge/Test Data")])
    data_root = models.CharField(max_length=100)
    branding_folder = models.CharField(max_length=100)
    branding_file = models.CharField(max_length=100, choices=[(file["name"],file["name"]) for file in folder_files("/Doc Merge/Branding")])

