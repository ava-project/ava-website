from django.contrib import auth
from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import DetailView, RedirectView, TemplateView, View

from . import forms
from .models import EmailValidationToken, Device


class RegisterView(FormView):
    """
    This endpoint is a generic form view for the user
    registration. The validation of the form is done
    by the validators on the model layer. Then it
    creates the user, the validation token and it
    sends the email, then redirect to the homepage
    """

    template_name = "user/register.html"
    form_class = forms.RegisterForm

    @transaction.atomic
    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'],
            data['email'],
            data['password']
        )
        EmailValidationToken.create_and_send_validation_email(user)
        return redirect('main:index')


class ProfileView(TemplateView):
    """
    This endpoint allows one to see his profile and
    edit his parameters.
    """
    template_name = "user/profile.html"


"""
This endpoint allows one to see his profile and
edit his parameters.
"""
class ProfileEditView(UpdateView):
    template_name = "user/edit-profile.html"
    form_class = forms.EditProfileForm
    success_url = reverse_lazy('user:profile')

    def get_object(self):
        return self.request.user


class ValidateTokenEmailView(TemplateView):
    """
    This endpoint tests if the token is in the database and
    if it's not expired, correspond to the correct user and
    if it's not consumed yet, then the user account will be
    validate after that
    """

    def get(self, request, **kwargs):
        try:
            token = EmailValidationToken.objects.get(token=request.GET['token'])
            if not token.is_valid(request.GET['email']):
                raise Exception('invalid token')
            token.consume()
            return redirect('main:index')
        except:
            return HttpResponseBadRequest('Something went wrong with your token, please try again')


class ResendValidationEmail(View):
    """
    This endpoint sends another email to validate the account
    of one person who didn't validated
    """

    def get(self, request, **kwargs):
        user = request.user
        if not user.profile.validated:
            EmailValidationToken.create_and_send_validation_email(user)
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
