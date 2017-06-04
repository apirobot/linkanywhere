from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from linkanywhere.apps.users.views import FacebookLogin, GoogleLogin, VKLogin
from .routers import router

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),

    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb-login'),
    url(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google-login'),
    url(r'^rest-auth/vk/$', VKLogin.as_view(), name='vk-login'),

    url(r'^admin/', admin.site.urls),
    url(r'^django-rq/', include('django_rq.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
