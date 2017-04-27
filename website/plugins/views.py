from django.db import transaction
from django.shortcuts import render
from django.views.generic import FormView

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
        plugin = self.get_plugin(data_plugin['manifest']['name'])
        plugin.upload_from_manifest(data_plugin['manifest'])
        plugin.save()
        nb_release = Release.objects.filter(plugin=plugin).count() + 1
        Release(
            plugin=plugin,
            version=nb_release,
            archive=data_plugin['zipfile']).save()
        return super().form_valid(form)

    def get_success_url(self):
        return '/'
