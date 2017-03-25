from django.utils import crypto

def generate_token():
    return crypto.get_random_string(length=50)
