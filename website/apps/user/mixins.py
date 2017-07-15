from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

class LoginMixin(object):

    def login_user(self, user):
        user.backend = 'user.backend.AuthenticationBackend'
        if user:
            login(self.request, user)


class UserMustBeValidated(object):

    def get_redirection_url(self):
        return reverse('user:profile', args=(self.request.user.username,))

    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.validated:
            return super().dispatch(*args, **kwargs)
        messages.error(self.request,
            'You must validated your account with your email.')
        return redirect(self.get_redirection_url())


class JsonUserMustBeValidated(object):

    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.validated:
            return super().dispatch(*args, **kwargs)
        return HttpResponseForbidden('You must validate your account with your email.')
