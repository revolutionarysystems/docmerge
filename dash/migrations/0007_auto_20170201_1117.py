# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-01 11:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0006_auto_20160619_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mergejob',
            name='branding_file',
            field=models.CharField(choices=[('--', '--')], max_length=100),
        ),
        migrations.AlterField(
            model_name='mergejob',
            name='data_file',
            field=models.CharField(choices=[('--', '--')], max_length=100),
        ),
        migrations.AlterField(
            model_name='mergejob',
            name='flow',
            field=models.CharField(choices=[('--', '--')], max_length=100),
        ),
        migrations.AlterField(
            model_name='mergejob',
            name='template',
            field=models.CharField(choices=[('--', '--')], max_length=100),
        ),
        migrations.AlterField(
            model_name='mergejob',
            name='template_subfolder',
            field=models.CharField(choices=[('--', '--')], max_length=100),
        ),
        migrations.AlterField(
            model_name='mergejob',
            name='xform_file',
            field=models.CharField(choices=[('--', '--'), ('None', 'None')], max_length=100),
        ),
    ]
