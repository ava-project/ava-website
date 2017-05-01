from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, DetailView

from . import forms
from .models import Plugin, Release


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


class PluginDetailView(DetailView):
    model = Plugin
    template_name = 'plugins/detail.html'

    def get_object(self, queryset=None):
        kwargs = {
            'author__username': self.kwargs['username'],
            'name': self.kwargs['plugin_name']
        }
        queryset = self.model.objects
        return get_object_or_404(queryset, **kwargs)
