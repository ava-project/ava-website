import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .uploads import open_file
from ..models import Plugin

url_upload = reverse('plugins:upload')


class DownloadPluginTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('username', 'email@email.fr', 'password')
        self.user.profile.validated = True
        self.user.profile.save()
        self.client.force_login(self.user)
        with open_file('good_plugin.zip') as plugin:
            resp = self.client.post(url_upload, {'archive': plugin})
            print(resp)

    def test_generate_url(self):
        plugin = Plugin.objects.first()
        url = plugin.url_download
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content_json = json.loads(response.content)
        response = self.client.get(content_json['url'])
        self.assertEqual(response.status_code, 200)
