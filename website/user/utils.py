from django.utils import crypto

from core.utils import send_email

def create_and_send_validation_email(user):
    # avoid circular import
    from .models import EmailValidationToken

    token = EmailValidationToken(user=user)
    token.save()
    send_email(
        'email/user_register.html',
        user.email,
        token=token)

def generate_token():
    return crypto.get_random_string(length=50)
