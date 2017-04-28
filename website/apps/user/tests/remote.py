from django.core import mail
from django.test import TestCase, Client
from django.contrib.auth.models import User

from ..forms import RegisterForm

class RemoteEndpointTest(TestCase):

    def setUp(self):
        User.objects.create_user('username', 'email@email.fr', 'password')
        self.client = Client()

    def test_wrong_credentials(self):
        form_data = {
            'email': 'wrong',
            'password': 'wrong'
        }
        response = self.client.post('/user/login.json', form_data)
        self.assertEqual(response.status_code, 400)

    def test_right_crendentials(self):
        form_data = {
            'email': 'email@email.fr',
            'password': 'password'
        }
        response = self.client.post('/user/login.json', form_data)
        self.assertEqual(response.status_code, 200)
