import os

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Plugin(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def update_from_manifest(self, manifest):
        """
        This fonction update the plugin information from the manifest file
        """
        manifest['description'] = "TODO IMPLEMENT DESCRIPTION"
        self.description = manifest['description']

    @property
    def url(self):
        return reverse('plugins:detail', args=[self.author.username, self.name])


def plugin_directory_path(instance, filename):
    filename = '{}.zip'.format(str(instance.version))
    return 'plugins/{}/{}/{}'.format(instance.plugin.author.username, instance.plugin.name, filename)


class Release(models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    version = models.IntegerField(default=0)
    archive = models.FileField(upload_to=plugin_directory_path)
