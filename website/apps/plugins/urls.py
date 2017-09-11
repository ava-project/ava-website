from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views, views_remote
from user.decorators import remote_login_required

app_name = 'plugins'

urlpatterns = [
    url(r'^upload/?$',
        login_required(views.UploadPluginView.as_view()),
        name='upload'),
    url(r'^my-plugins/?$',
        remote_login_required(views_remote.MyPluginListView.as_view()),
        name='my-list'),
    url(r'^list/?$',
        views.PluginListView.as_view(),
        name='list'),
    url(r'^list.json/?$',
        views_remote.PluginListView.as_view(),
        name='list-json'),
    url(r'^download/(?P<token>[^/]+)/?$',
        remote_login_required(views_remote.PluginDownloadLinkView.as_view()),
        name='download-link'),
    url(r'^(?P<username>[^/]+)/(?P<plugin_name>[^/]+)/',
        include([
            url(r'^$',
                views.PluginDetailView.as_view(),
                name='detail'),
            url(r'^upvote/?$',
                login_required(views.PluginUpvoteView.as_view()),
                name='upvote'),
            url(r'^downvote/?$',
                login_required(views.PluginDownvoteView.as_view()),
                name='downvote'),
            url(r'^json/?$',
                views_remote.PluginDetailView.as_view(),
                name='detail-json'),
            url(r'^download/?$',
                remote_login_required(views_remote.PluginDownloadView.as_view()),
                name='download'),
            url(r'^download/(?P<version>[^/]+)/$',
                remote_login_required(views_remote.PluginDownloadView.as_view()),
                name='download-version'),
        ])
    ),
]
