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
