from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class AuthenticationBackend(ModelBackend):
    """
    Join the request with the profile
    """

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.\
                select_related('profile').\
                get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class EmailBackend(AuthenticationBackend):
    """
    Login with the email address and normal password
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            is_active = getattr(user, 'is_active', False)
            if is_active and user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            pass
        return None
