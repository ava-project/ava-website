# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-16 23:16
from __future__ import unicode_literals

from django.db import migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_emailvalidationtoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailvalidationtoken',
            name='expire',
        ),
        migrations.AddField(
            model_name='emailvalidationtoken',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='emailvalidationtoken',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
    ]