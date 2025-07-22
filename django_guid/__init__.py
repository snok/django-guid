import django

from django_guid.api import clear_guid, get_guid, set_guid  # noqa F401

__version__ = '3.5.2'

if django.VERSION < (3, 2):
    default_app_config = 'django_guid.apps.DjangoGuidConfig'

__all__ = ['clear_guid', 'get_guid', 'set_guid']
