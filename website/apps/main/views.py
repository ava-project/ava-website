from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, View

from .models import OperatingSystem, CoreInstaller


class DownloadView(ListView):
    template_name = 'main/download.html'
    model = OperatingSystem


class DownloadReleaseView(View):

    def get(self, request, **kwargs):
        release = get_object_or_404(CoreInstaller, pk=self.kwargs['pk'])
        binary = release.binary
        response = HttpResponse(binary.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'inline; filename=' + binary.name
        return response
