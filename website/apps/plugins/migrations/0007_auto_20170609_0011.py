# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-09 00:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plugins', '0006_userplugins'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userplugins',
            unique_together=set([('plugin', 'user')]),
        ),
    ]
