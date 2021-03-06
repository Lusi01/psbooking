import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .settings_base import *


DEBUG = False
ALLOWED_HOSTS = ['34.88.24.61', 'localhost']
SITE_ID = 2
SOCIAL_AUTH_VK_OAUTH2_KEY = env('VK_APP_ID')
SOCIAL_AUTH_VK_OAUTH2_SECRET = env('VK_API_SECRET')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '',
    }
}

STATIC_ROOT = BASE_DIR / 'staticfiles' #os.path.join(BASE_DIR, 'static')
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Настройка MEDIA файлов
MEDIA_ROOT = BASE_DIR / 'media'
#MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",
)
