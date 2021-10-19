"""
Django settings for psbooking project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/


psBooking
http://localhost

psBooking

Права:
Отправка писем через Яндекс.Почту по протоколу SMTP

Доступ к адресу электронной почты

Callback URL:
Время жизни токена: Не менее, чем 1 год
Дата создания: 18.08.2021


"""
import os
import environ
from pathlib import Path
from django.urls import reverse_lazy


env = environ.Env(  # set casting, default value
    DEBUG=(bool, False))
# reading .env file
environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# для DEBUG:
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True
ALLOWED_HOSTS = []

# DEBUG = False
# ALLOWED_HOSTS = ['127.0.0.1']

# # Для Product
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
# ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['127.0.0.1',]
# # #ALLOWED_HOSTS = ['192.168.1.34', '127.0.0.1']


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = reverse_lazy('accounts:sign_in')

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

SITE_ID = 2  #1  #https://www.youtube.com/watch?v=kBNUGLVJoOo

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth', # Фреймворк аутентификации и моделей по умолчанию.
    'django.contrib.contenttypes', # Django контент-типовая система (даёт разрешения, связанные с моделями).
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Extra Django apps
    'django.contrib.sites', # стандартное приложение Django - для allauth

    # Third Party apps
    'django_cleanup',  # .apps.CleanupConfig',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.vk', #https://habr.com/ru/sandbox/48565/

    # 'debug_toolbar',

    #'bootstrap_modal_forms',

    # project apps
    'main.apps.MainConfig',
    'hotels.apps.HotelsConfig',  # 'hotels',
    'accounts.apps.AccountsConfig',
    'mail.apps.MailConfig',
]

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Управление сессиями между запросами
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Связывает пользователей, использующих сессии, запросами.
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'psbooking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # где хранятся шаблоны
        #'DIRS': [BASE_DIR / 'templates'],
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                #'django.template.context_processors.media',
            ],
            'libraries': {
                    'psbookingtags': 'templatetags.psbookingtags',
                    'mytags': 'templatetags.mytags',
                }
        },
    },
]

# TEMPLATE_CONTEXT_PROCESSORS = (
#     'django.core.context_processors.media',
# )

WSGI_APPLICATION = 'psbooking.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    #необходим для входа в админ.часть сайта под username для админа.
    # Должен быть независимо от 'allauth'
    'django.contrib.auth.backends.ModelBackend',

    # кастомный бакенд вместо стандартного 'django.contrib.auth.backends.ModelBackend'
    # пример: https://rahmanfadhil.com/django-login-with-email/
    'accounts.backends.EmailBackend', # кастомный бакенд вместо стандартного

    # Специальные методы аутентификации 'allauth', такие как вход в систему по эл.почте
    'allauth.account.auth_backends.AuthenticationBackend',
)

# REST_FRAMEWORK = {
#     'DEFAULT_FILTER_BACKENDS': (
#         'django_filters.rest_framework.DjangoFilterBackend',
#     )
# }

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-Ru'    #'en-us'

TIME_ZONE = 'UTC' # 'Europe/Moscow'

USE_I18N = True

USE_L10N = False #чтобы digital выводился по 'en-us'

USE_TZ = True

DECIMAL_SEPARATOR = '.'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# эта настройка для production!
#STATIC_ROOT = BASE_DIR / 'static' #os.path.join(BASE_DIR, 'static')
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/' #префикс URL адреса статического файла
# Настройка поисковика для папок статики
# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [STATIC_DIR] #[os.path.join(BASE_DIR, 'static'), ]

# эта папка, куда создаем файлы для разработки
STATICFILES_DIRS = [
    BASE_DIR / 'assets/'
]

# Настройка MEDIA файлов
MEDIA_ROOT = BASE_DIR / 'media'
#MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import django_heroku
django_heroku.settings(locals())

INTERNAL_IPS = [
    '127.0.0.1',
]