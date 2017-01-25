from django.conf.urls import url
from django.contrib.auth import views as django_auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # before authentication
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
    # change password
    url(r'^password-reset/?$',
        django_auth_views.password_reset,
        name='reset-password'),
    url(r'^password-reset/done?$',
        django_auth_views.password_reset_done,
        name='reset-password-done'),
    # token validation
    url(r'^resend_validation_email/?$',
        login_required(views.ResendValidationEmail.as_view()),
        name='resend-validation-email'),
    url(r'^validate_email/?$',
        views.ValidateTokenEmailView.as_view(),
        name='validate-email'),
]
