from django.contrib.auth.models import User
from django.db import models
from django.utils import crypto, timezone
from model_utils.models import TimeStampedModel

def generate_token():
    return crypto.get_random_string(length=50)

def generate_expiration():
    timezone.now() + datetime.timedelta(days=14)

# class Device(TimeStampedModel, models.Model):
#     NB_DAY_EXPIRE = 2
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     token = models.CharField(max_length=50, default=generate_token, unique=True)
