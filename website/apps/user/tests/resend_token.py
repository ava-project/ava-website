import datetime

from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from ..models import EmailValidationToken

"""
Test if validation email is correctly sent when
you hit the endpoint, by counting the number of
email sent
"""
class ResendValidationEmailTest(TestCase):

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
        self.client.login(username='correct', password='test')

    def test_resend_creation(self):
        self.assertEqual(len(mail.outbox), 1)
        url = reverse('user:resend-validation-email')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 2)


"""
Make sure the email is not sent if the account is already
activated
"""
class ResendValidationEmailForAccountActivatedTest(TestCase):

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
        self.user.profile.validated = True
        self.user.profile.save()
        self.client.login(username='correct', password='test')

    def test_resend_creation(self):
        self.assertEqual(len(mail.outbox), 1)
        url = reverse('user:resend-validation-email')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
