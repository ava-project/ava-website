from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class UsernameValidator(RegexValidator):
    regex = '^[a-zA-Z0-9_.-]+$'
    message = 'Enter a valid value.'
