import datetime

from django.utils import timezone
from model_utils.models import TimeStampedModel

class Expirationable():
    NB_DAY_EXPIRE = 2

    def is_expired(self):
        limit = self.created + datetime.timedelta(days=self.NB_DAY_EXPIRE)
        if limit < timezone.now():
            return True
        return False
