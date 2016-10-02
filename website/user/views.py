from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from core.utils import send_email

from . import forms
from .models import EmailValidationToken

"""
This endpoint is a generic form view for the user
registration. The validation of the form is done
by the validators on the model layer. Then it
creates the user, the validation token and it
sends the email, then redirect to the homepage
"""
class RegisterView(FormView):
    template_name = "generic/form.html"
    form_class = forms.RegisterForm

    def send_validation_email(self, user, token):
        send_email(
            'user/email_register.html',
            user.email,
            token=token)

    @transaction.atomic
    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'],
            data['email'],
            data['password']
        )
        token = EmailValidationToken(user=user)
        token.save()
        self.send_validation_email(user, token)
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
        except Exception as e:
            return HttpResponseBadRequest('Something went wrong with your token, please try again')
