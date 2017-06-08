import datetime

from django.utils import timezone


class Expirationable():
    NB_DAY_EXPIRE = 2
    NB_MINUTE_EXPIRE = 0

    def is_expired(self):
        timediff = datetime.timedelta(days=self.NB_DAY_EXPIRE)
        if self.NB_MINUTE_EXPIRE:
            timediff += datetime.timedelta(minutes=self.NB_MINUTE_EXPIRE)
        limit = self.created + timediff
        if limit < timezone.now():
            return True
        return False
