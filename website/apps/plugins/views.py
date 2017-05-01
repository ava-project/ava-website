from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, DetailView, View

from . import forms, mixins
from .models import Plugin, Release, DownloadRelease


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


class PluginDetailView(mixins.PluginDetailMixin, DetailView):
    template_name = 'plugins/detail.html'


class PluginDownloadView(mixins.PluginDetailMixin, View):

    @transaction.atomic
    def get(self, request, **kwargs):
        plugin = self.get_object()
        release = plugin.release_set.order_by('version').first()
        download = DownloadRelease(plugin=plugin, release=release,
            author=self.request.user)
        download.save()
        return JsonResponse({
            'url': download.url
        })


class PluginDownloadLinkView(View):

    def get(self, request, **kwargs):
        download = get_object_or_404(DownloadRelease, token=self.kwargs['token'])
        archive = download.release.archive
        response = HttpResponse(archive.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'inline; filename=' + archive.name
        return response