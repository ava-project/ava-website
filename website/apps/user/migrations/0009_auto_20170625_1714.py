# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 17:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_forbiddenusername'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forbiddenusername',
            old_name='token',
            new_name='username',
        ),
    ]
