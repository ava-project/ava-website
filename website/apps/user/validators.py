from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


from .models import ForbiddenUsername


class UsernameValidator(RegexValidator):
    regex = '^[a-z0-9-]+$'
    message = 'Username can only contains a-z, -, 0-9'


def emailUniqueValidator(email):
    if email and User.objects.filter(email=email).count():
        raise ValidationError(u'A user with that email address already exists.')


def blacklistUsername(username):
    if ForbiddenUsername.objects.filter(username=username).count():
        raise ValidationError(u'You can\'t use that username')
