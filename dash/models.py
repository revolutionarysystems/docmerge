from django.db import models

class MergeJob(models.Model):

    template_folder = models.CharField(max_length=100)
    template = models.CharField(max_length=100)
    flow = models.CharField(max_length=100)
    output_folder = models.CharField(max_length=100)
    ident = models.CharField(max_length=100)
