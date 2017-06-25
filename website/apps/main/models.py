from django.db import models
import os
from model_utils.models import TimeStampedModel

from stdimage.models import StdImageField


class OperatingSystem(models.Model):
    name = models.CharField(max_length=120)
    image = StdImageField(upload_to='os_logo',
                          null=True,
                          variations={'thumbnail':
                            {'width': 100, 'height': 100}})

    def __str__(self):
        return self.name


def installer_directory_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    filename = 'ava_{}_{}{}'.format(instance.os.name, str(instance.version), extension)
    return 'core_installer/{}/{}'.format(instance.os.name, filename)


class CoreInstaller(TimeStampedModel, models.Model):
    os = models.ForeignKey(OperatingSystem, on_delete=models.CASCADE)
    binary = models.FileField(upload_to=installer_directory_path)
    instruction = models.TextField(default='')
    version = models.CharField(max_length=40)
