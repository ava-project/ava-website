import os

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

url = reverse('plugins:upload')
base_path = os.path.dirname(os.path.realpath(__file__)) + '/assets'

good_plugin_hash = 'c48afac6604666fa0983fee4d85d893834963fb65bab5858ae7071550e9025a5'

def open_file(name):
    return open('{}/{}'.format(base_path, name), 'rb')


class UploadPluginTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('username', 'email@email.fr', 'password')
        self.user.profile.validated = True
        self.user.profile.save()
        self.client.force_login(self.user)

    def test_no_input(self):
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<li>This field is required.</li>')

    def test_not_a_zip(self):
        with open_file('wrong_format.txt') as plugin:
            response = self.client.post(url, {'archive': plugin})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '<li>Only zip archived are allowed</li>')

    def test_bad_archive(self):
        with open_file('wrong_format.zip') as plugin:
            response = self.client.post(url, {'archive': plugin})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '<li>Bad .zip format</li>')

    def test_no_config_file_archive(self):
        with open_file('no_config_file.zip') as plugin:
            response = self.client.post(url, {'archive': plugin})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '<li>No manifest.json found in archive</li>')

    def test_bad_format_config_file_archive(self):
        with open_file('bad_format_json.zip') as plugin:
            response = self.client.post(url, {'archive': plugin})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '<li>Error with manifest.json, bad Json Format</li>')

    def test_bad_config_file_archive(self):
        with open_file('bad_config.zip') as plugin:
            response = self.client.post(url, {'archive': plugin})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Error in manifest.json')

    def test_good_archive(self):
        with open_file('good_plugin.zip') as plugin:
            response = self.client.post(url, {'archive': plugin})
            self.assertEqual(response.status_code, 302)
