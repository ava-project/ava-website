from django.db import transaction, IntegrityError
from django.db.models import F
from django.http import HttpResponseBadRequest,\
    JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, DetailView, ListView, View
from django.urls import reverse

from . import forms, mixins
from .models import Plugin, Release, Upvote,\
    DownloadRelease, UserPlugins, UserPlugins


class UploadPluginView(FormView):
    template_name = 'plugins/upload.html'
    form_class = forms.UploadPluginForm

    def get_plugin(self, name):
        try:
            return Plugin.objects.get(name=name)
        except Plugin.DoesNotExist:
            return Plugin(name=name, author=self.request.user)

    @transaction.atomic
    def form_valid(self, form):
        data_plugin = form.cleaned_data['archive']
        self.plugin = self.get_plugin(data_plugin['manifest']['name'])
        self.plugin.update_from_manifest(data_plugin['manifest'])
        self.plugin.save()
        nb_release = Release.objects.filter(plugin=self.plugin).count() + 1
        Release(
            plugin=self.plugin,
            version=nb_release,
            archive=data_plugin['zipfile']).save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.plugin.url


class PluginListView(ListView):
    model = Plugin
    template_name = 'plugins/list.html'


class PluginDetailView(mixins.PluginDetailMixin, DetailView):
    template_name = 'plugins/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_has_upvoted'] = self.object.user_has_upvoted(self.request.user)
        return context


class PluginUpvoteView(mixins.PluginDetailMixin, View):

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        plugin = self.get_object()
        params = {'user': request.user, 'plugin': plugin}
        if Upvote.objects.filter(**params).count() == 0:
            Upvote.objects.create(**params)
            plugin.nb_upvote = F('nb_upvote') + 1
            plugin.save(update_fields=['nb_upvote'])
        return redirect(plugin.url)


class PluginDownvoteView(mixins.PluginDetailMixin, View):

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        plugin = self.get_object()
        params = {'user': request.user, 'plugin': plugin}
        if Upvote.objects.filter(user=request.user, plugin=plugin).delete()[0] == 1:
            plugin.nb_upvote = F('nb_upvote') - 1
            plugin.save(update_fields=['nb_upvote'])
        return redirect(plugin.url)


class JsonPluginDetailView(mixins.PluginDetailMixin, View):

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
        if not 'version' in self.kwargs:
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
            'version': release.version,
        })


class PluginDownloadLinkView(View):

    def add_download(self, plugin, user):
        params = {'user': user, 'plugin': plugin}
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
        self.add_download(download.plugin, request.user)
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
        return {
            'author': username,
            'name': name,
            'url': reverse('plugins:download', args=(username, name)),
        }

    def get(self, request, **kwargs):
        plugins = UserPlugins.objects.filter(user=request.user)
        return JsonResponse([self.generate_plugin_data(plugin) for plugin in plugins], safe=False)
