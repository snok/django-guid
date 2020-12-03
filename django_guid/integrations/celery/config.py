# flake8: noqa: D102
from typing import TYPE_CHECKING

from django.core.exceptions import ImproperlyConfigured

from django_guid.integrations import SentryIntegration

if TYPE_CHECKING:
    from django_guid.integrations.celery import CeleryIntegration  # pragma: no cover


class CeleryIntegrationSettings:
    def __init__(self, instance: 'CeleryIntegration') -> None:
        self.instance = instance
        self.validate()

    @property
    def use_django_logging(self) -> bool:
        return self.instance.use_django_logging

    @property
    def log_parent(self) -> bool:
        return self.instance.log_parent

    @property
    def uuid_length(self) -> int:
        return self.instance.uuid_length

    @property
    def sentry_integration(self) -> bool:
        return self.instance.sentry_integration

    def validate(self) -> None:
        if not isinstance(self.use_django_logging, bool):
            raise ImproperlyConfigured('The CeleryIntegration use_django_logging setting must be a boolean.')
        if not isinstance(self.log_parent, bool):
            raise ImproperlyConfigured('The CeleryIntegration log_parent setting must be a boolean.')
        if type(self.uuid_length) is not int or not 1 <= self.uuid_length <= 32:
            raise ImproperlyConfigured('The CeleryIntegration uuid_length setting must be an integer.')
        if not isinstance(self.sentry_integration, bool):
            raise ImproperlyConfigured('The CeleryIntegration sentry_integration setting must be a boolean.')
        if self.sentry_integration:
            SentryIntegration().setup()
