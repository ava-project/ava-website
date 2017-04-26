from django.shortcuts import render
from django.views.generic import FormView

from . import forms


class UploadPluginView(FormView):
    template_name = 'plugins/upload.html'
    form_class = forms.UploadPluginForm

    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        return super().form_valid(form)
