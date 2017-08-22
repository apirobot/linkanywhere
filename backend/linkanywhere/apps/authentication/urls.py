from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token
from djoser import views as djoser_views

urlpatterns = [
    url(
        r'^auth/token/obtain/$',
        obtain_jwt_token,
        name='obtain_token'
    ),
    url(
        r'^auth/register/$',
        djoser_views.RegistrationView.as_view(),
        name='register'
    ),
    url(
        r'^auth/password/reset/$',
        djoser_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    url(
        r'^auth/password/reset/confirm/$',
        djoser_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
]
