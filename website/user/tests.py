import unittest
from django.test import Client

class DuplicateTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_register(self):
        # Issue a GET request.
        response = self.client.post('/user/register/', {
            'username': 'test',
            'email': 'test@test.fr',
            'password': 'test',
        })
        self.assertEqual(response.status_code, 302)
