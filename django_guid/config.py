# flake8: noqa: D102
from typing import List, Union

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.inspect import func_accepts_kwargs

from django_guid.integrations.celery import CeleryIntegrationSettings


class IntegrationSettings:
    def __init__(self, integration_settings: dict) -> None:
        if integration_settings is None:
            integration_settings = {}
        self.settings = integration_settings

    @property
    def celery(self) -> CeleryIntegrationSettings:
        return CeleryIntegrationSettings(self.settings.get('CeleryIntegration', {}))

    def validate(self):
        self.celery.validate()


class Settings:
    """
    Settings for django_guid read from the Django settings in `settings.py`.

    Inspired by django-auth-adfs from @jobec
    """

    def __init__(self) -> None:
        if hasattr(django_settings, 'DJANGO_GUID'):
            self.settings = django_settings.DJANGO_GUID
        else:
            self.settings = {}

    @property
    def GUID_HEADER_NAME(self) -> str:
        return self.settings.get('GUID_HEADER_NAME', 'Correlation-ID')

    @property
    def RETURN_HEADER(self) -> bool:
        return self.settings.get('RETURN_HEADER', True)

    @property
    def EXPOSE_HEADER(self) -> bool:
        return self.settings.get('EXPOSE_HEADER', True)

    @property
    def IGNORE_URLS(self) -> List[str]:
        return list({url.strip('/') for url in self.settings.get('IGNORE_URLS', [])})

    @property
    def VALIDATE_GUID(self) -> bool:
        return self.settings.get('VALIDATE_GUID', True)

    @property
    def INTEGRATIONS(self) -> Union[list, tuple]:
        return self.settings.get('INTEGRATIONS', [])

    @property
    def INTEGRATION_SETTINGS(self):
        """
        When implementing integration settings we had one challenge: some settings were needed in the integration
        instance's setup method while others were needed in code imported in integration.setup().
        This creates a circularity challenge in terms of how we initialize settings.
        If we:
         1. Loaded everything into the integration instance, the imported code would not be able to access it,
            without importing the integration, which is not possible.
         2. Used the `DJANGO_GUID` dict in settings.py and loaded settings here, we wouldn't be able
            to access them in the integration instace without breaking backwards compatibility and
            getting a lot of integration-specific logic in the package-level config file which we don't want.

        What we ended up with is loading everything into to integration instance *and* saving the instance here
        while changing the settings from eager to lazy, so they're not accessed before they've initialized.
        """
        return IntegrationSettings({integration.identifier: integration for integration in self.INTEGRATIONS})

    def validate(self):
        if not isinstance(self.VALIDATE_GUID, bool):
            raise ImproperlyConfigured('VALIDATE_GUID must be a boolean')
        if not isinstance(self.GUID_HEADER_NAME, str):
            raise ImproperlyConfigured('GUID_HEADER_NAME must be a string')  # Note: Case insensitive
        if not isinstance(self.RETURN_HEADER, bool):
            raise ImproperlyConfigured('RETURN_HEADER must be a boolean')
        if not isinstance(self.EXPOSE_HEADER, bool):
            raise ImproperlyConfigured('EXPOSE_HEADER must be a boolean')
        if not isinstance(self.INTEGRATIONS, (list, tuple)):
            raise ImproperlyConfigured('INTEGRATIONS must be an array')
        if not isinstance(self.IGNORE_URLS, (list, tuple)):
            raise ImproperlyConfigured('IGNORE_URLS must be an array')
        if not all(isinstance(url, str) for url in self.IGNORE_URLS):
            raise ImproperlyConfigured('IGNORE_URLS must be an array of strings')

        self._validate_and_setup_integrations()

    def _validate_and_setup_integrations(self) -> None:
        """
        Validate the INTEGRATIONS settings and verify each integration
        """
        self.INTEGRATION_SETTINGS.validate()
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


settings = Settings()
