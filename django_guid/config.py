from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured


class Settings(object):
    """
    Settings for django_guid read from the Django settings in `settings.py`.

    Inspired by django-auth-adfs from @jobec
    """

    def __init__(self) -> None:
        self.GUID_HEADER_NAME = 'Correlation-ID'
        self.VALIDATE_GUID = True
        self.SKIP_CLEANUP = False
        self.RETURN_HEADER = True
        self.EXPOSE_HEADER = True

        if hasattr(django_settings, 'DJANGO_GUID'):
            _settings = django_settings.DJANGO_GUID

            # Set user settings if provided
            for setting, value in _settings.items():
                if hasattr(self, setting):
                    setattr(self, setting, value)
                else:
                    raise ImproperlyConfigured(f'{setting} is not a valid setting for django_guid')

            if not isinstance(self.SKIP_CLEANUP, bool):
                raise ImproperlyConfigured('SKIP_CLEANUP must be a boolean')
            if not isinstance(self.VALIDATE_GUID, bool):
                raise ImproperlyConfigured('VALIDATE_GUID must be a boolean')
            if not isinstance(self.GUID_HEADER_NAME, str):
                raise ImproperlyConfigured('GUID_HEADER_NAME must be a string')  # Note: Case insensitive
            if not isinstance(self.RETURN_HEADER, bool):
                raise ImproperlyConfigured('RETURN_HEADER must be a boolean')
            if not isinstance(self.EXPOSE_HEADER, bool):
                raise ImproperlyConfigured('EXPOSE_HEADER must be a boolean')
        else:
            pass  # Do nothing if DJANGO_GUID not found in settings


settings = Settings()
