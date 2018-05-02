"""
Django settings for home project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import json
# import datetime

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

# import uwsgi
# from uwsgidecorators import timer
# from django.utils import autoreload

# @timer(3)
# def change_code_gracefull_reload(sig):
#     if autoreload.code_changed():
#         uwsgi.reload()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Env for dev / deploy
# def get_env(setting, envs):
#     try:
#         return envs[setting]
#     except KeyError:
#         error_msg = "You SHOULD set {} environ".format(setting)
#         raise ImproperlyConfigured(error_msg)

# # SocialLogin: Soundcloud
SOCIAL_AUTH_SOUNDCLOUD_KEY = "7c76b10fd87a3f9cf91d51b9f8cf069c"
SOCIAL_AUTH_SOUNDCLOUD_SECRET = "8ea6d6ffda811dda41c13f0125376b21"

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_AUTHENTICATED_LOGOUT_REDIRECTS = True
# ACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'

SOCIALACCOUNT_EMAIL_VERIFICATION  = 'none'
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Dopehotz] "
ACCOUNT_EMAIL_REQUIRED = True
DEFAULT_FROM_EMAIL = 'info@dopehotz.com'
# ACCOUNT_AUTHENTICATION_METHOD = "username|email"

ACCOUNT_LOGOUT_REDIRECT_URL = "/callback/"

SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/callback/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_PROVIDERS = {
    'authentiq': {
      'SCOPE': ['email', 'aq:name']
    }
}

# LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/accounts/auth-validation/'

ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = LOGIN_REDIRECT_URL


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zj7+c4182z+f$^t#76(x@l7&aytzjx7p-1aekeh%7ds0pd_sa7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
APPEND_SLASH = True
# CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = ['api.dopehotz.com', 'adm.dopehotz.com', 'dopehotz.com', 'auth.dopehotz.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    #custom app
    'accounts.apps.AccountsConfig',
    'tracks.apps.TracksConfig',
    'articles.apps.ArticlesConfig',
    'playlists.apps.PlaylistsConfig',

    #third party
    'debug_toolbar',
    'django_hosts',
    'rest_framework',
    'rest_framework.authtoken',
    # 'social_django',
    'rangefilter',
    'daterange_filter',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.facebook',
]

SITE_ID  =  3

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    #custom middleware
    'accounts.middleware.AuthLogMiddleware',
]

SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True
# SESSION_COOKIE_DOMAIN = '.dopehotz.com'
# CSRF_COOKIE_DOMAIN = '.dopehotz.com'

# 서브도메인 url 매칭
ROOT_URLCONF = 'home.urls'
ADMIN_URLCONF = 'home.admin_urls'
AUTH_URLCONF = 'home.auth_urls'

ROOT_HOSTCONF = 'home.hosts'
DEFAULT_HOST = 'api'

CORS_ORIGIN_WHITELIST = (
    'localhost',
    '127.0.0.1',
    'dopehotz.com',
    'angular.dopehotz.com',
    'angular.dopehotz.com'
)

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ALLOW_HEADERS = (
#     'accept',
#     'accept-encoding',
#     'authorization',
#     'content-type',
#     'dnt',
#     'origin',
#     'user-agent',
#     'x-csrftoken',
#     'x-requested-with',
# )

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'home.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dopehotz',
        'USER': 'dopehotz',
        'PASSWORD': 'dopehotz!@010506150707',
        'HOST': '',
        'PORT' : '',
        'OPTIONS': {
            'charset': 'utf8',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_unicode_ci',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'accounts.User'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'
# LANGUAGES = [
#   ('ko', _('Korean')),
#   ('en', _('English')),
# ]
# LOCALE_PATHS = (
#     os.path.join(BASE_DIR, 'locale'),
# )

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'assets')
]

# STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# 사이트 정보
SITE_NAME = 'DOPEHOTZ'
SITE_URL = '//api.dopehotz.com'
MAIN_URL = 'https://dopehotz.com'

ADMIN_SITE_HEADER = SITE_NAME+" 관리"
ADMIN_SITE_TITLE = SITE_NAME+" 사이트 관리"


INTERNAL_IPS = ['211.220.213.125', '59.20.199.142', '49.143.106.133', '1.215.108.44',]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES' : [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # 'home.authentication.ExpiringTokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}
REST_FRAMEWORK_TOKEN_EXPIRE_HOURS = 24


AUTHENTICATION_BACKENDS = [
    # 'social_core.backends.facebook.FacebookOAuth2', # Facebook
    # 'social_core.backends.soundcloud.SoundcloudOAuth2', # Soundcloud
    # 'social_core.backends.naver.NaverOAuth2', # Soundcloud

    # 'accounts.auth.SettingsBackend',
    'django.contrib.auth.backends.ModelBackend', # Django 기본 유저모델
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'accounts.social.create_user', # 덮어씀
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
