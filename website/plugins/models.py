from django.contrib.auth.models import User
from django.db import models


class Plugin(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def upload_from_manifest(self, manifest):
        manifest['description'] = "TODO IMPLEMENT DESCRIPTION"
        self.description = manifest['description']


class Release(models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    version = models.IntegerField(default=0)
    archive = models.FileField(upload_to='plugins/')
