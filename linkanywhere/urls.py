from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^api/v1/', include('linkanywhere.apps.links.urls', namespace='links')),
    url(r'^api/v1/', include('linkanywhere.apps.users.urls', namespace='users')),

    url(r'^admin/', admin.site.urls),
    url(r'^django-rq/', include('django_rq.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
