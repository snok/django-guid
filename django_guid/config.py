from warnings import warn

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.inspect import func_accepts_kwargs


class Settings(object):
    """
    Settings for django_guid read from the Django settings in `settings.py`.

    Inspired by django-auth-adfs from @jobec
    """

    def __init__(self) -> None:
        self.GUID_HEADER_NAME = 'Correlation-ID'
        self.VALIDATE_GUID = True
        self.RETURN_HEADER = True
        self.EXPOSE_HEADER = True
        self.INTEGRATIONS = []
        self.SKIP_CLEANUP = None  # Deprecated - to be removed in the next major version

        if hasattr(django_settings, 'DJANGO_GUID'):
            _settings = django_settings.DJANGO_GUID

            # Set user settings if provided
            for setting, value in _settings.items():
                if hasattr(self, setting):
                    setattr(self, setting, value)
                else:
                    raise ImproperlyConfigured(f'{setting} is not a valid setting for django_guid')

            if not isinstance(self.VALIDATE_GUID, bool):
                raise ImproperlyConfigured('VALIDATE_GUID must be a boolean')
            if not isinstance(self.GUID_HEADER_NAME, str):
                raise ImproperlyConfigured('GUID_HEADER_NAME must be a string')  # Note: Case insensitive
            if not isinstance(self.RETURN_HEADER, bool):
                raise ImproperlyConfigured('RETURN_HEADER must be a boolean')
            if not isinstance(self.EXPOSE_HEADER, bool):
                raise ImproperlyConfigured('EXPOSE_HEADER must be a boolean')
            if not isinstance(self.INTEGRATIONS, list):
                raise ImproperlyConfigured('INTEGRATIONS must be an array')

            for integration in self.INTEGRATIONS:

                # Make sure all integration methods are callable
                for method, name in [
                    (integration.setup, 'setup'),
                    (integration.run, 'run'),
                    (integration.cleanup, 'cleanup'),
                ]:
                    # Make sure the methods are callable
                    if not callable(method):
                        raise ImproperlyConfigured(
                            f'Integration method `{name}` needs to be made callable for `{integration.identifier}`.'
                        )

                    # Make sure the method takes kwargs
                    if name in ['run', 'cleanup'] and not func_accepts_kwargs(method):
                        raise ImproperlyConfigured(
                            f'Integration method `{name}` must '
                            f'accept keyword arguments (**kwargs) for `{integration.identifier}`.'
                        )

                # Run validate method
                integration.setup()

            if 'SKIP_CLEANUP' in _settings:
                warn(
                    'SKIP_CLEANUP was deprecated in v1.2.0, and no longer impacts package behaviour. '
                    'Please remove it from your DJANGO_GUID settings.',
                    DeprecationWarning,
                )


settings = Settings()
