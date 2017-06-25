from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name="main/index.html"),
        name='index'),
    url(r'^download/?$',
        views.DownloadView.as_view(),
        name='download'),
    url(r'^download/(?P<pk>[^/]+)?$',
        views.DownloadReleaseView.as_view(),
        name='download-release'),
]
