from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from . import forms
from .models import EmailValidationToken


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
        EmailValidationToken(user=user).save()
        return redirect('main:index')


"""
This endpoint tests if the token is in the database and
if it's not expired, correspond to the correct user and
if it's not consumed yet, then the user account will be
validate after that
"""
class ValidateTokenEmailView(TemplateView):

    def get(self, request, **kwargs):
        try:
            token = EmailValidationToken.objects.get(token=request.GET['token'])
            if not token.is_valid(request.GET['email']):
                raise Exception('invalid token')
            token.consume()
            return redirect('main:index')
        except Exception:
            return 'hehehe'
