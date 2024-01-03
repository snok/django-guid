# flake8: noqa: D102
from collections import defaultdict
from typing import Dict, List, Union

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.inspect import func_accepts_kwargs

from django_guid.integrations.celery.config import CeleryIntegrationSettings


class IntegrationSettings:
    def __init__(self, integration_settings: dict) -> None:
        self.settings = integration_settings

    @property
    def celery(self) -> CeleryIntegrationSettings:
        return CeleryIntegrationSettings(self.settings['CeleryIntegration'])

    def validate(self) -> None:
        if 'CeleryIntegration' in self.settings:
            self.celery.validate()


class Settings:
    def __init__(self) -> None:
        if hasattr(django_settings, 'DJANGO_GUID'):
            self.settings = django_settings.DJANGO_GUID
        else:
            self.settings = {}

    @property
    def guid_header_name(self) -> str:
        return self.settings.get('GUID_HEADER_NAME', 'Correlation-ID')

    @property
    def return_header(self) -> bool:
        return self.settings.get('RETURN_HEADER', True)

    @property
    def expose_header(self) -> bool:
        return self.settings.get('EXPOSE_HEADER', True)

    @property
    def ignore_urls(self) -> List[str]:
        return list({url.strip('/') for url in self.settings.get('IGNORE_URLS', [])})

    @property
    def validate_guid(self) -> bool:
        return self.settings.get('VALIDATE_GUID', True)

    @property
    def integrations(self) -> Union[list, tuple]:
        return self.settings.get('INTEGRATIONS', [])

    @property
    def integration_settings(self) -> IntegrationSettings:
        return IntegrationSettings({integration.identifier: integration for integration in self.integrations})

    @property
    def uuid_length(self) -> int:
        default_length: Dict[str, int] = defaultdict(lambda: 32, string=36)
        return self.settings.get('UUID_LENGTH', default_length[self.uuid_format])

    @property
    def uuid_format(self) -> str:
        return self.settings.get('UUID_FORMAT', 'hex')

    def validate(self) -> None:
        if not isinstance(self.validate_guid, bool):
            raise ImproperlyConfigured('VALIDATE_GUID must be a boolean')
        if not isinstance(self.guid_header_name, str):
            raise ImproperlyConfigured('GUID_HEADER_NAME must be a string')  # Note: Case insensitive
        if not isinstance(self.return_header, bool):
            raise ImproperlyConfigured('RETURN_HEADER must be a boolean')
        if not isinstance(self.expose_header, bool):
            raise ImproperlyConfigured('EXPOSE_HEADER must be a boolean')
        if not isinstance(self.integrations, (list, tuple)):
            raise ImproperlyConfigured('INTEGRATIONS must be an array')
        if not isinstance(self.settings.get('IGNORE_URLS', []), (list, tuple)):
            raise ImproperlyConfigured('IGNORE_URLS must be an array')
        if not all(isinstance(url, str) for url in self.settings.get('IGNORE_URLS', [])):
            raise ImproperlyConfigured('IGNORE_URLS must be an array of strings')
        if type(self.uuid_length) is not int or self.uuid_length < 1:
            raise ImproperlyConfigured('UUID_LENGTH must be an integer and positive')
        if self.uuid_format == 'string' and not 1 <= self.uuid_length <= 36:
            raise ImproperlyConfigured('UUID_LENGTH must be between 1-36 when UUID_FORMAT is string')
        if self.uuid_format == 'hex' and not 1 <= self.uuid_length <= 32:
            raise ImproperlyConfigured('UUID_LENGTH must be between 1-32 when UUID_FORMAT is hex')
        if self.uuid_format not in ('hex', 'string'):
            raise ImproperlyConfigured('UUID_FORMAT must be either hex or string')

        self._validate_and_setup_integrations()

    def _validate_and_setup_integrations(self) -> None:
        """
        Validate the INTEGRATIONS settings and verify each integration
        """
        self.integration_settings.validate()
        for integration in self.integrations:
            # Make sure all integration methods are callable
            for method, name in [
                (integration.setup, 'setup'),
                (integration.run, 'run'),
                (integration.cleanup, 'cleanup'),
            ]:
                # Make sure the methods are callable
                if not callable(method):
                    raise ImproperlyConfigured(
                        f'Integration method `{name}` needs to be made callable for `{integration.identifier}`'
                    )

                # Make sure the method takes kwargs
                if name in ['run', 'cleanup'] and not func_accepts_kwargs(method):
                    raise ImproperlyConfigured(
                        f'Integration method `{name}` must '
                        f'accept keyword arguments (**kwargs) for `{integration.identifier}`'
                    )

            # Run validate method
            integration.setup()


settings = Settings()
