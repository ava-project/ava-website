from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager

from core.behaviors import Expirationable
from main.utils import generate_token


class Plugin(TimeStampedModel, models.Model):
    name = models.CharField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    nb_download = models.IntegerField(default=0)
    nb_upvote = models.IntegerField(default=0)

    @property
    def url(self):
        return reverse('plugins:detail', args=[self.author.username, self.name])

    @property
    def url_download(self):
        return reverse('plugins:download', args=[self.author.username, self.name])

    @property
    def last_release(self):
        return self.release_set.order_by('-created').first()

    def get_release(self, version=None):
        if version:
            return self.release_set.filter(version=version).first()
        return self.last_release

    def user_has_upvoted(self, user):
        if not user.is_authenticated():
            return False
        query = Upvote.objects.filter(plugin=self, user=user)
        return True if query.count() else False


def plugin_directory_path(instance, filename):
    filename = '{}.zip'.format(str(instance.version))
    return 'plugins/{}/{}/{}'.format(instance.plugin.author.username, instance.plugin.name, filename)


class Release(TimeStampedModel, models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    version = models.IntegerField(default=0)
    archive = models.FileField(upload_to=plugin_directory_path)
    description = models.TextField(default='')
    readme = models.TextField(default='')
    readme_html = models.TextField(default='')
    tags = TaggableManager()


class PluginCommand(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(default='')


class DownloadRelease(Expirationable, TimeStampedModel, models.Model):
    NB_DAY_EXPIRE = 0
    NB_MINUTE_EXPIRE = 5

    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, default=generate_token)
    is_used = models.BooleanField(default=False)

    @property
    def url(self):
        return reverse('plugins:download-link',
            args=[self.token])


class UserPlugins(TimeStampedModel, models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('plugin', 'user')


class Upvote(TimeStampedModel, models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('plugin', 'user')
