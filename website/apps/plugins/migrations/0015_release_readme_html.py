# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-24 04:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0014_release_readme'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='readme_html',
            field=models.TextField(default=''),
        ),
    ]