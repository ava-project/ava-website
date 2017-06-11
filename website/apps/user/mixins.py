from django.contrib.auth import login


class LoginMixin(object):

    def login_user(self, user):
        user.backend = 'user.backend.AuthenticationBackend'
        if user:
            login(self.request, user)
