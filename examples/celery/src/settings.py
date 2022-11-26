import os
from typing import List

from celery.schedules import crontab

from django_guid.integrations import CeleryIntegration

# fmt: off

# No values are required
DJANGO_GUID = {
    'INTEGRATIONS': [
        CeleryIntegration(
            use_django_logging=True,
            log_parent=True,
            uuid_length=10
        )
    ]
}

CELERY_BROKER_URL = 'redis://:@localhost:6378'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_BEAT_SCHEDULE = {
    'test': {
        'task': 'src.celery.debug_task',
        'schedule': crontab(minute='*/1'),
    },
}

# Log filter setup is required
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'correlation_id': {'()': 'django_guid.log_filters.CorrelationId'},  # <-- Add correlation ID
        'celery_tracing': {'()': 'django_guid.integrations.celery.log_filters.CeleryTracing'},  # <-- Add celery IDs
    },
    'formatters': {
        # Example of a basic log format without correlation ID filter
        'basic_format': {'format': '%(levelname)s %(asctime)s %(name)s - %(message)s'},

        # Example format with correlation ID
        'correlation_id': {
            'format': '%(levelname)s %(asctime)s [%(correlation_id)s] %(name)s - %(message)s'  # <-- Add the %(correlation_id)s
        },

        # Format with correlation ID plus a celery process' parent ID and a unique current ID that will
        # become the parent ID of any child processes that are created (most likely you won't want to
        # display these values in your formatter, but include them just as a filter)
        'celery_depth_format': {
            'format': '%(levelname)s [%(correlation_id)s] [%(celery_parent_id)s-%(celery_current_id)s] %(name)s - %(message)s'
        },
    },
    'handlers': {
        'correlation_id_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'correlation_id',
            'filters': ['correlation_id'],  # <-- Add this filter here
        },
        'celery_depth_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'celery_depth_format',
            'filters': ['correlation_id', 'celery_tracing'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['correlation_id_handler'],  # <-- Add the handler in your loggers
            'level': 'INFO'
        },
        'src': {
            'handlers': ['celery_depth_handler'],
            'level': 'DEBUG'
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
