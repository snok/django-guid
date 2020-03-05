from warnings import warn

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
        self.RETURN_HEADER = True
        self.EXPOSE_HEADER = True
        self.INTEGRATE_SENTRY = False
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
            if not isinstance(self.INTEGRATE_SENTRY, bool):
                raise ImproperlyConfigured('INTEGRATE_SENTRY must be a boolean')

            if 'SKIP_CLEANUP' in _settings:
                warn(
                    'SKIP_CLEANUP was deprecated in v1.2.0, and no longer impacts package behaviour. '
                    'Please remove it from your DJANGO_GUID settings.',
                    DeprecationWarning,
                )

            if self.INTEGRATE_SENTRY:
                if self.GUID_HEADER_NAME != 'X-Transaction-ID':
                    # Sentry's standard header name is X-Transaction-ID, so make sure we're using the same header value to
                    # enable the middlewares _get_id_from_header-function to work properly
                    raise ImproperlyConfigured('To integrate with Sentry, the GUID_HEADER_NAME needs to be set to `X-Transaction-ID`')

                # Make sure the sentry_sdk is installed, so we can use it in middleware.py
                try:
                    import sentry_sdk
                except ModuleNotFoundError:
                    raise ImproperlyConfigured('The `sentry-sdk` package needs to be installed to integrate with Sentry. '
                                               'Please run `pip install sentry-sdk`, or set `INTEGRATE_SENTRY` to False in the settings.')



settings = Settings()
