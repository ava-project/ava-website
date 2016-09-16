from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from . import forms


class RegisterView(FormView):
    template_name = "user/register.html"
    form_class = forms.RegisterForm

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'],
            data['email'],
            data['password']
        )
        return redirect('main:index')


class ValidateTokenEmail(TemplateView):
    pass
