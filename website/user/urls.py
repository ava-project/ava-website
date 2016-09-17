from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/?$',
        views.RegisterView.as_view(),
        name='register'),
    url(r'^validate_email/?$',
        views.ValidateTokenEmailView.as_view(),
        name='validate-email'),
]
