from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'plugins'

urlpatterns = [
    url(r'^upload/?$',
        login_required(views.UploadPluginView.as_view()),
        name='upload'),
    url(r'^download/(?P<token>[^/]+)/?$',
        login_required(views.PluginDownloadLinkView.as_view()),
        name='download-link'),
    url(r'^(?P<username>[^/]+)/(?P<plugin_name>[^/]+)/?',
        include([
            url(r'^$',
                views.PluginDetailView.as_view(),
                name='detail'),
            url(r'^download/?$',
                login_required(views.PluginDownloadView.as_view()),
                name='download'),
        ])
    ),
]
