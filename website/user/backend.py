from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

"""
Join the request with the profile
"""
class AuthenticationBackend(ModelBackend):

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.\
                select_related('profile').\
                get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class EmailBackend(AuthenticationBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            return user if getattr(user, 'is_active', False)\
                and user.check_password(password) else None
        except UserModel.DoesNotExist:
            return None
