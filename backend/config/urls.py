from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

# Register API
apipatterns = [
    url(r'^', include('linkanywhere.apps.authentication.urls')),
    url(r'^', include('linkanywhere.apps.categories.urls')),
    url(r'^', include('linkanywhere.apps.links.urls')),
    url(r'^', include('linkanywhere.apps.tags.urls')),
    url(r'^', include('linkanywhere.apps.users.urls')),
]

urlpatterns = [

    url(r'^api/v1/', include((apipatterns, 'api'), namespace='api')),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

    if 'rest_framework_swagger' in settings.INSTALLED_APPS:
        from rest_framework_swagger.views import get_swagger_view
        schema_view = get_swagger_view(title='Linkanywhere API')
        urlpatterns = [
            url(r'^docs/$', schema_view),
            url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        ] + urlpatterns
