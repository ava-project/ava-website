import datetime

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from model_utils.models import TimeStampedModel

from core.behaviors import Expirationable

from .utils import generate_token


class Device(Expirationable, TimeStampedModel, models.Model):
    """
    Represent a Daemon using the JSON API
    """
    NB_DAY_EXPIRE = 14 # expire after 2 weeks

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, default=generate_token, unique=True)


class Profile(TimeStampedModel, models.Model):
    """
    Extend the User model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    validated = models.BooleanField(default=False)
    email_await_validation = models.EmailField(blank=True)


class EmailValidationToken(Expirationable, TimeStampedModel, models.Model):
    """
    Store the tokens for validating account
    """
    token = models.CharField(max_length=50, default=generate_token, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    consumed = models.BooleanField(default=False)

    def is_valid(self, email):
        if self.consumed\
            or email != self.user.profile.email_await_validation\
            or self.is_expired():
            return False
        return True

    def consume(self):
        self.user.profile.validated = True
        self.user.profile.save()
        self.user.email = self.user.profile.email_await_validation
        self.consumed = True
        self.save()


"""
Signal to create a profile model when a User is created
"""
@receiver(post_save, sender=User)
def after_user_save(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        profile = Profile(user=user, email_await_validation=user.email)
        profile.save()
