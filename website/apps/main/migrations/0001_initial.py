# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 13:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models
import model_utils.fields
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstallerFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('binary', models.FileField(upload_to=main.models.installer_directory_path)),
                ('version', models.CharField(max_length=40)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OperatingSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('image', stdimage.models.StdImageField(null=True, upload_to='os_logo')),
            ],
        ),
        migrations.AddField(
            model_name='installerfiles',
            name='os',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.OperatingSystem'),
        ),
    ]
