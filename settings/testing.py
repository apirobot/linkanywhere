from .local import Local


class Testing(Local):

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
        'DEFAULT_FILTER_BACKENDS': (
            'django_filters.rest_framework.DjangoFilterBackend',
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        )
    }
