from django.db import transaction
from django.db.models import F, Q
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import FormView, DetailView, ListView, View

from . import forms, mixins
from .models import Plugin, Release, Upvote


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
        self.plugin.save()
        nb_release = Release.objects.filter(plugin=self.plugin).count() + 1
        release = Release(
            plugin=self.plugin,
            version=nb_release,
            description=data_plugin['manifest'].get('description', ''),
            archive=data_plugin['zipfile'])
        if data_plugin['readme']:
            release.set_readme(data_plugin['readme'])
        release.save()
        if 'tags' in data_plugin['manifest']:
            release.add_tags(data_plugin['manifest']['tags'])
        release.add_commands(data_plugin['manifest'].get('commands', []))
        return super().form_valid(form)

    def get_success_url(self):
        return self.plugin.url


class PluginListView(ListView):
    model = Plugin
    template_name = 'plugins/list.html'
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if not search:
            return super().get_queryset()
        query = Q(name__icontains=search)
        query |= Q(author__username__startswith=search)
        return self.model.objects.filter(query)


class PluginDetailView(mixins.PluginDetailMixin, DetailView):
    template_name = 'plugins/detail.html'

    def get_release(self):
        return self.object.get_release(self.request.GET.get('version', None))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_has_upvoted'] = self.object.user_has_upvoted(self.request.user)
        context['release'] = self.get_release()
        if not context['release']:
            raise Http404('Can\'t find this version')
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
        if Upvote.objects.filter(user=request.user, plugin=plugin).delete()[0] == 1:
            plugin.nb_upvote = F('nb_upvote') - 1
            plugin.save(update_fields=['nb_upvote'])
        return redirect(plugin.url)
