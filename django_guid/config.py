from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured


class Settings(object):
    """
    Settings for django_guid read from the Django settings in `settings.py`
    Inspired by django-auth-adfs from @jobec
    """

    def __init__(self):
        self.GUID_HEADER_NAME = 'Correlation-ID'  # Required
        self.VALIDATE_GUID = True

        required_settings = [
            'GUID_HEADER_NAME'
        ]

        if not hasattr(django_settings, 'DJANGO_GUID'):
            raise ImproperlyConfigured('DJANGO_GUID settings not found.')
        _settings = django_settings.DJANGO_GUID

        # Set user settings if provided
        for setting, value in _settings.items():
            if hasattr(self, setting):
                setattr(self, setting, value)
            else:
                raise ImproperlyConfigured(f'{setting} is not a valid setting for django_guid.')

        if not isinstance(self.VALIDATE_GUID, bool):
            raise ImproperlyConfigured('VALIDATE_GUID must be a boolean.')
        if not isinstance(self.GUID_HEADER_NAME, str):
            raise ImproperlyConfigured('GUID_HEADER_NAME must be a string')  # Note: Case insensitive

        for setting in required_settings:
            if not getattr(self, setting):
                raise ImproperlyConfigured(f'django_guid setting {setting} must be set.')


settings = Settings()
