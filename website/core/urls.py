from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'', include('main.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^plugins/', include('plugins.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]
