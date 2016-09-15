from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class RegisterView(TemplateView):
    template_name = "user/register.html"

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)
