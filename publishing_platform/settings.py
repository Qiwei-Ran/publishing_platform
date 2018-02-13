"""
Django settings for publishing_platform project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jji)r3ywp@dmagx$yvcfu6$$=_oh98r%a_wbsyqp+%64)_i%u8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['2.2.2.100']

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'bootstrapform',
    'pagination',
    'rest_framework',
    'rest_framework_swagger',
    'web',
    'users',
    'perms',
    'config',
    'log',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # page
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'publishing_platform.urls'

# noinspection SpellCheckingInspection
WSGI_APPLICATION = 'publishing_platform.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'publishing_platform',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '2.2.2.100',
        'PORT': '3306',
    }
}

# Internationalization
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# setting about Static file (CSS, JavaScript, Images)
# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Upload dir setting
upload_path = "%s/upload/" % BASE_DIR
MEDIA_ROOT = upload_path
MEDIA_URL = '/upload/'

# Template setting
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        # 'DEBUG': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
            ],
        },
    },
]

# Auth and Login setting
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = "/users/login/"
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/accounts/profile/'

# Log config setting
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # log filter
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    # log handler for handle log
    'handlers': {
        # send erro log to mail
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        # send debug log to console
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/publishing_platform/main.log',
            'formatter': 'simple',
        },
    },
    # logger for get log and set log_level
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'publishing_platform.web.view': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    # formatters of the log format
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s  %(levelname)s  %(message)s'
        },
    },
}

# use to send email to user
EMAIL_HOST = 'mail.qq.com'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'devops'
EMAIL_HOST_PASSWORD = '123456'
EMAIL_USE_TLS = False
EMAIL_PUSH = False  # True
SendMail = "ops@xxx.com"

CONFIG = type('_', (), {'__getattr__': lambda arg1, arg2: None})()

# The rest_framework of Django
REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'users.permissions.IsSuperUser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authentication.AccessKeyAuthentication',
        'users.authentication.AccessTokenAuthentication',
        'users.authentication.PrivateTokenAuthentication',
        'users.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}
