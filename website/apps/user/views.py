"""
Django view of the user app.
List of classes:
- RegisterView
- ProfileView
- ProfileEditView
- ValidateTokenEmailView
- ResendValidationEmailView
"""

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import DetailView, TemplateView, View

from . import forms
from .mixins import LoginMixin
from .models import EmailValidationToken


class RegisterView(LoginMixin, SuccessMessageMixin, FormView):
    """
    This endpoint is a generic form view for the user registration.
    """

    template_name = "user/register.html"
    form_class = forms.RegisterForm
    success_message = 'Account created, welcome to the team !'

    @transaction.atomic
    def form_valid(self, form):
        """
        Create user after form validation.
        Send the validation token.
        Redirect to the home page.
        """
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'],
            data['email'],
            data['password']
        )
        EmailValidationToken.create_and_send_validation_email(user, self.request)
        self.login_user(user)
        return redirect('main:index')


class ProfileView(DetailView):
    """
    This endpoint allows one to see his profile.
    """
    template_name = "user/profile.html"
    model = User

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])


class ProfileEditView(UpdateView):
    """
    This endpoint allows user to edit his profile.
    """
    template_name = "user/edit-profile.html"
    form_class = forms.EditProfileForm
    success_message = 'Profile updated'

    def get_success_url(self):
        return self.request.user.profile_url()

    def get_object(self, queryset=None):
        """Return the current user."""
        return self.request.user


class ValidateTokenEmailView(LoginMixin, View):
    """
    View validating token received by email.
    """

    def get(self, request, **kwargs):
        """
        Validate account from link sent by email.

        This endpoint tests if the token is in the database and
        if it's not expired, correspond to the correct user and
        if it's not consumed yet, then the user account will be
        validate after that.
        """
        try:
            token = EmailValidationToken.objects.get(token=request.GET['token'])
            if not token.is_valid(request.GET['email']):
                raise ValueError('invalid token')
            token.consume()
            if not request.user.is_authenticated:
                self.login_user(token.user)
            messages.success(request, 'Email validated')
            return redirect('main:index')
        except (EmailValidationToken.DoesNotExist, ValueError) as e:
            print(e)
            return HttpResponseBadRequest('Something went wrong with your token, please try again')


class ResendValidationEmailView(View):
    """
    This endpoint sends another email to validate the account
    of one person who didn't validated
    """

    def get(self, request, **kwargs):
        user = request.user
        if not user.profile.validated:
            EmailValidationToken.create_and_send_validation_email(user, request)
            messages.success(request, 'Validation email resent')
        return redirect(user.profile_url())


def profile_url(self):
    return reverse('user:profile', args=[self.username])

User.add_to_class('profile_url', profile_url)
