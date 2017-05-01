from django.shortcuts import get_object_or_404

from .models import Plugin

class PluginDetailMixin(object):
    model = Plugin

    def get_object(self, queryset=None):
        kwargs = {
            'author__username': self.kwargs['username'],
            'name': self.kwargs['plugin_name']
        }
        queryset = self.model.objects
        return get_object_or_404(queryset, **kwargs)
