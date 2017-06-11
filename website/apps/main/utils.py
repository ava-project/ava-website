from django.utils import crypto


def generate_token(length=50):
    return crypto.get_random_string(length=length)
