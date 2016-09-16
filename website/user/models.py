import datetime

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone, crypto


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    validated = models.BooleanField(default=False)


class EmailValidationToken(models.Model):
    token = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expire = models.DateTimeField()
    consumed = models.BooleanField(default=False)

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
        Profile(user=kwargs['instance']).save()
        EmailValidationToken(user=kwargs['instance']).save()
