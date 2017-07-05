from django.db import transaction
from django.db.models import F
from django.http import HttpResponseBadRequest,\
    JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.urls import reverse

from . import mixins
from .models import Release, DownloadRelease, UserPlugins


class PluginDetailView(mixins.PluginDetailMixin, View):

    def get(self, *args, **kwargs):
        plugin = self.get_object()
        return JsonResponse({
            'name': plugin.name,
            'author': plugin.author.username,
            'last_version': plugin.release_set.order_by('-version').first().version,
            'versions': list(plugin.release_set.values_list('version', flat=True)),
        })


class PluginDownloadView(mixins.PluginDetailMixin, View):

    def get_release(self, plugin):
        if 'version' not in self.kwargs:
            return plugin.release_set.order_by('-version').first()
        return plugin.release_set.get(version=int(self.kwargs['version']))

    @transaction.atomic
    def get(self, request, **kwargs):
        plugin = self.get_object()
        try:
            release = self.get_release(plugin)
        except Release.DoesNotExist:
            return HttpResponseBadRequest('Can\'t find this version')
        download = DownloadRelease(plugin=plugin, release=release,
            author=self.request.user)
        download.save()
        return JsonResponse({
            'url': download.url,
            'checksum': release.checksum,
            'version': release.version,
        })


class PluginDownloadLinkView(View):

    def add_download(self, plugin, user, release):
        params = {'user': user, 'plugin': plugin, 'release': release}
        if UserPlugins.objects.filter(**params).count() == 0:
            UserPlugins.objects.create(**params)

    @transaction.atomic
    def get(self, request, **kwargs):
        download = get_object_or_404(DownloadRelease, token=self.kwargs['token'])
        if request.user != download.author:
            return HttpResponseForbidden('You are not authorized to download this plugin')
        if download.is_expired() or download.is_used:
            return HttpResponse('Expired link', status=410)
        download.is_used = True
        download.save()
        download.plugin.nb_download = F('nb_download') + 1
        download.plugin.save(update_fields=['nb_download'])
        self.add_download(download.plugin, request.user, download.release)
        archive = download.release.archive
        response = HttpResponse(archive.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'inline; filename=' + archive.name
        return response


class MyPluginListView(View):
    """
    This endpoint retrieves the list of plugins the user installed
    """

    def generate_plugin_data(self, plugin):
        username = plugin.plugin.author.username
        name = plugin.plugin.name
        release = plugin.release if plugin.release else plugin.plugin.last_release
        return {
            'author': username,
            'name': name,
            'version': release.version,
            'url': reverse('plugins:download', args=(username, name)),
        }

    def get(self, request, **kwargs):
        plugins = UserPlugins.objects.filter(user=request.user)
        return JsonResponse([self.generate_plugin_data(plugin) for plugin in plugins], safe=False)
