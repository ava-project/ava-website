from django.core import mail
from django.test import TestCase, Client
from django.contrib.auth.models import User

from ..forms import RegisterForm


class RegisterTest(TestCase):

    def setUp(self):
        User.objects.create_user('username', 'email@email.fr', 'password')
        self.client = Client()

    def test_200_form(self):
        response = self.client.get('/user/register')
        self.assertEqual(response.status_code, 200)

    def test_correct_registration(self):
        form_data = {
            'username': 'correct',
            'email': 'correct@email.fr',
            'password': 'test',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post('/user/register', form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

    def test_empty_username(self):
        form_data = {
            'username': '',
            'email': 'empty_username@email.fr',
            'password': 'test',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_empty_email(self):
        form_data = {
            'username': 'empty_email',
            'email': '',
            'password': 'test',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_empty_password(self):
        # empty username
        form_data = {
            'username': 'empty_password',
            'email': 'empty_password@email.fr',
            'password': '',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_duplicate_email(self):
        form_data = {
            'username': 'different',
            'email': 'email@email.fr',
            'password': 'test',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_duplicate_username(self):
        form_data = {
            'username': 'username',
            'email': 'different@different.fr',
            'password': 'test',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
