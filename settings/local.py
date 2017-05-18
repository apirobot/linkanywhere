from configurations import values

from .common import *  # noqa


class Local(Common):

    DEBUG = values.BooleanValue(True)
    for config in Common.TEMPLATES:
        config['OPTIONS']['debug'] = DEBUG

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('django_nose', 'django_extensions', 'autofixture')
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

    # Mail
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = values.Value('django.core.mail.backends.console.EmailBackend')

    # Vesitle Image Field settings
    VERSATILEIMAGEFIELD_SETTINGS = Common.VERSATILEIMAGEFIELD_SETTINGS
    VERSATILEIMAGEFIELD_SETTINGS['create_images_on_demand'] = True

    # Django RQ local settings
    RQ_QUEUES = {
        'default': {
            'URL': env('REDISTOGO_URL', default='redis://localhost:6379'),
            'DB': 0,
            'DEFAULT_TIMEOUT': 500,
        },
    }
