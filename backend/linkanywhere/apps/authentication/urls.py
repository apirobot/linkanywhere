from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(
        r'^auth/token/obtain/$',
        obtain_jwt_token,
        name='obtain_token'
    ),
]
