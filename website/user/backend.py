from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

"""
Join the request with the profile
"""
class AuthenticationBackend(ModelBackend):

    def get_user(self, user_id):
        try:
            return User.objects.\
                select_related('profile').\
                get(pk=user_id)
        except User.DoesNotExist:
            return None
