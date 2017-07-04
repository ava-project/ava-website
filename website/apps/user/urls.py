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
        views.LoginView.as_view(),
        name='login'),
    url(r'^logout/?$',
        django_auth_views.logout,
        name='logout'),
    # password reset
    url(r'^reset-password/?$',
        django_auth_views.password_reset,
        name='password_reset',
        kwargs={
            'post_reset_redirect': 'user:password_reset_done',
            'email_template_name': 'email/password_reset_email.html',
        }),
    url(r'^reset-password/done/?$',
        django_auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^reset-link/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        django_auth_views.password_reset_confirm,
        name='password_reset_confirm',
        kwargs={
            'post_reset_redirect': 'user:password_reset_complete',
        }),
    url(r'^reset-password/compete/?$',
        django_auth_views.password_reset_complete,
        name='password_reset_complete'),

    # profile
    url(r'^profile/edit/?$',
        login_required(views.ProfileEditView.as_view()),
        name='edit-profile'),
    url(r'^profile/password-change/?$',
        login_required(django_auth_views.password_change),
        name='password_change',
        kwargs={
            'template_name': 'user/edit-password.html',
            'post_change_redirect': 'user:password_change_done',
        }),
    url(r'^profile/password-change/done/?$',
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

    url(r'^(?P<username>[a-zA-Z0-9-]+)/?$',
        views.ProfileView.as_view(),
        name='profile'),
]
