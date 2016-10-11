from core.utils import send_email

from .models import EmailValidationToken

def create_and_send_validation_email(user):
    token = EmailValidationToken(user=user)
    token.save()
    send_email(
        'email/user_register.html',
        user.email,
        token=token)
