from django.conf.urls import url
from django.contrib.auth import views as django_auth_views
from django.contrib.auth.decorators import login_required

from . import views, views_remote
from .decorators import remote_login_required

app_name = 'user'


urlpatterns = [
    # changing visitor state
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

    # profile
    url(r'^profile/?$',
        login_required(views.ProfileView.as_view()),
        name='profile'),
    url(r'^profile/edit/?$',
        login_required(views.ProfileEditView.as_view()),
        name='edit-profile'),
    url(r'^profile/password_change/?$',
        login_required(django_auth_views.password_change),
        name='password_change',
        kwargs={
            'template_name': 'user/edit-password.html',
            'post_change_redirect': 'user:password_change_done',
        }),
    url(r'^profile/password_change/done/?$',
        login_required(django_auth_views.password_change_done),
        name='password_change_done',
        kwargs={
            'template_name': 'user/edit-password-done.html',
        }),

    # token validation
    url(r'^resend_validation_email/?$',
        login_required(views.ResendValidationEmailView.as_view()),
        name='resend-validation-email'),
    url(r'^validate_email/?$',
        views.ValidateTokenEmailView.as_view(),
        name='validate-email'),

    # for json api
    url(r'^login.json/?$',
        views_remote.RemoteLoginView.as_view(),
        name='login-json'),
    url(r'^me.json/?$',
        remote_login_required(views_remote.RemoteInfoUserView.as_view()),
        name='me-json'),
    url(r'^logout.json/?$',
        remote_login_required(views_remote.RemoteLogoutView.as_view()),
        name='logout-json'),
]
