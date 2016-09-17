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
class ValidateTokenEmail(TemplateView):

    def get(self, request, **kwargs):
        try:
            # pull from url
            email = request.GET['email']
            value_token = request.GET['token']
            # test if valid
            token = EmailValidationToken.objects.get(token=value_token)
            if token.consumed or email == token.user.email or token.is_expired():
                raise Exception('invalid token')
            # update everything
            token.user.profile.validated = True
            token.user.profile.save()
            token.consumed = True
            token.save()
        except Exception:
            return 'hehehe'
