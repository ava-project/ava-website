import datetime

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone, crypto
from model_utils.models import TimeStampedModel


class Profile(TimeStampedModel, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    validated = models.BooleanField(default=False)
    email_await_validation = models.EmailField(blank=True)


class EmailValidationToken(TimeStampedModel, models.Model):
    NB_DAY_EXPIRE = 2

    token = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    consumed = models.BooleanField(default=False)

    def is_expired(self):
        limit = self.created + datetime.timedelta(days=self.NB_DAY_EXPIRE)
        if limit < timezone.now():
            return True
        return False

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

    def save(self, *args, **kwargs):
        self.token = crypto.get_random_string(length=50)
        self.expire = timezone.now() + datetime.timedelta(days=2)
        super().save(*args, **kwargs)


"""
Signal to create a profile model when a User is created
"""
@receiver(post_save, sender=User)
def after_user_save(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        profile = Profile(user=user, email_await_validation=user.email)
        profile.save()
