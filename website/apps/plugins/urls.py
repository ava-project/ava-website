from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'plugins'

urlpatterns = [
    url(r'^upload/?$',
        login_required(views.UploadPluginView.as_view()),
        name='upload'),
    url(r'^(?P<username>[^/]+)/(?P<plugin_name>[^/]+)/?$',
        views.PluginDetailView.as_view(),
        name='detail'),
]
