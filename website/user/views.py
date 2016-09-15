from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from . import forms


class RegisterView(TemplateView):
    template_name = "user/register.html"

    def register_user(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'],
            data['email'],
            data['password']
        )
        return redirect('main:index')

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = forms.RegisterForm()
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            return self.register_user(form)
        context['form'] = form
        return self.render_to_response(context)
