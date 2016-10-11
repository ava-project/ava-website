from django.conf.urls import url
from django.contrib.auth import views as django_auth_views
from . import views

urlpatterns = [
    url(r'^register/?$',
        views.RegisterView.as_view(),
        name='register'),
    url(r'^login/?$',
        django_auth_views.login,
        name='login',
        kwargs={
            'template_name': 'user/login.html'
        }),
    url(r'^logout/?$',
        django_auth_views.logout,
        name='logout'),
    url(r'^validate_email/?$',
        views.ValidateTokenEmailView.as_view(),
        name='validate-email'),
]
