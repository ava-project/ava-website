from django.conf.urls import url
from django.views.generic import TemplateView

app_name = 'main'
urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name="main/index.html"),
        name='index'),
]
