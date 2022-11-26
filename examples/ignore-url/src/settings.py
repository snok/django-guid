import os
from typing import List

# fmt: off

# No values are required
DJANGO_GUID = {
    'IGNORE_URLS': ['ignored'],
}

# Log filter setup is required
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'correlation_id': {'()': 'django_guid.log_filters.CorrelationId'},  # <-- Add correlation ID
    },
    'formatters': {
        # Example of a basic log format without correlation ID filter
        'basic_format': {'format': '%(levelname)s %(asctime)s %(name)s - %(message)s'},

        # Example format with correlation ID
        'correlation_id': {
            'format': '%(levelname)s %(asctime)s [%(correlation_id)s] %(name)s - %(message)s'  # <-- Add the %(correlation_id)s
        },
    },
    'handlers': {
        'correlation_id_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'correlation_id',
            'filters': ['correlation_id'],  # <-- Add this filter here
        },
    },
    'loggers': {
        'django': {
            'handlers': ['correlation_id_handler'],  # <-- Add the handler in your loggers
            'level': 'INFO'
        },
        'src': {
            'handlers': ['correlation_id_handler'],
            'level': 'DEBUG'
        },
        'django_guid': {
            'handlers': ['correlation_id_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# fmt: on


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'secret'

DEBUG = True

ALLOWED_HOSTS: List[str] = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_guid',
]

MIDDLEWARE = [
    'django_guid.middleware.guid_middleware',  # <-- Add middleware at the top of your middlewares
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': ':memory:',
    }
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
