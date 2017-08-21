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

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
