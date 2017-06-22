from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class UsernameValidator(RegexValidator):
    regex = '^[a-zA-Z0-9-]+$'
    message = 'Username can only contains a-z, A-Z, -, 0-9'


def emailUniqueValidator(email):
    if email and User.objects.filter(email=email).count():
        raise ValidationError(u'A user with that email address already exists.')
