from django.contrib.auth import authenticate, login


class LoginMixin(object):

    def login_user(self, user):
        user.backend = 'user.backend.AuthenticationBackend'
        if user:
            login(self.request, user)
