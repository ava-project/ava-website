"""
Django view of the user app.
List of classes:
- RegisterView
- ProfileView
- ProfileEditView
- ValidateTokenEmailView
- ResendValidationEmailView
- RemoteLoginView
- RemoteInfoUserView
- RemoteLogoutView
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import TemplateView, View

from . import forms
from .mixins import LoginMixin
from .backend import AuthenticationBackend
from .models import EmailValidationToken, Device


class RegisterView(LoginMixin, FormView):
    """
    This endpoint is a generic form view for the user registration.
    """

    template_name = "user/register.html"
    form_class = forms.RegisterForm

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


class ProfileView(TemplateView):
    """
    This endpoint allows one to see his profile.
    """

    template_name = "user/profile.html"


class ProfileEditView(UpdateView):
    """
    This endpoint allows user to edit his profile.
    """

    template_name = "user/edit-profile.html"
    form_class = forms.EditProfileForm
    success_url = reverse_lazy('user:profile')

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
        return redirect('user:profile')


class RemoteLoginView(View):
    """
    This Endpoint authenticate a user, and create a unique token.
    A client can use Http Basic Auth with email as username and this token as password to sign his requests
    This token expires after two weeks.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        username = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            device = Device(user=user)
            device.save()
            return JsonResponse({'data': device.token})
        return JsonResponse({'error': 'Wrong credentials'}, status=400)


class RemoteInfoUserView(View):
    """
    This endpoint returns a json object with user information
    """

    def get(self, request, **kwargs):
        user = request.user
        data = {
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return JsonResponse(data)


class RemoteLogoutView(View):
    """
    This endpoint logout a user by removing all tokens.
    """

    def get(self, request, **kwargs):
        Device.objects.filter(user=request.user).delete()
        logout(request)
        return JsonResponse({'data': 'You have been logged out'})
