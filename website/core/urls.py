from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'', include('main.urls', namespace='main')),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]
