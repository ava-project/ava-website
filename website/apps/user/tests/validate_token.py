import datetime

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from mock import patch

from ..models import EmailValidationToken


class ValidateTokenMixin(object):

    def create_user(self):
        form_data = {
            'username': 'correct',
            'email': 'correct@email.fr',
            'password': 'test',
        }
        response = self.client.post('/user/register', form_data)
        self.assertEqual(response.status_code, 302)
        return User.objects.get(username=form_data['username'])

    def setUp(self):
        self.client = Client()
        self.user = self.create_user()

    def get_tokens(self):
        return EmailValidationToken.objects.filter(user=self.user)


class ValidateTokenTest(ValidateTokenMixin, TestCase):

    def test_create_token(self):
        tokens = self.get_tokens()
        self.assertEqual(len(tokens), 1)

    def test_validate_token(self):
        token = self.get_tokens()[0]
        self.assertFalse(token.consumed)
        self.assertFalse(self.user.profile.validated)
        url = '/user/validate_email?email={}&token={}'
        self.client.get(url.format(self.user.email, token.token))
        token.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertTrue(token.consumed)
        self.assertTrue(self.user.profile.validated)


class ErrorTokenConsumedTest(ValidateTokenMixin, TestCase):

    def test_consume_twice(self):
        token = self.get_tokens()[0]
        self.assertTrue(token.is_valid(self.user.email))
        token.consume()
        self.assertFalse(token.is_valid(self.user.email))


class TokenOtherErrorTest(ValidateTokenMixin, TestCase):

    def test_bad_email(self):
        token = self.get_tokens()[0]
        self.assertFalse(token.is_valid('random_email@test.fr'))

    def test_expire(self):
        nb_day_expire = EmailValidationToken.NB_DAY_EXPIRE + 1
        new_now = timezone.now() + datetime.timedelta(days=nb_day_expire)
        token = self.get_tokens()[0]
        self.assertFalse(token.is_expired())
        with patch.object(timezone, 'now', return_value=new_now):
            token = self.get_tokens()[0]
            self.assertTrue(token.is_expired())
