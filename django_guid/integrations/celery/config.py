# flake8: noqa: D102
from typing import TYPE_CHECKING

from django.core.exceptions import ImproperlyConfigured

if TYPE_CHECKING:
    from django_guid.integrations.celery import CeleryIntegration


class CeleryIntegrationSettings:
    def __init__(self, integration: 'CeleryIntegration') -> None:
        self.integration = integration
        self.validate()

    @property
    def use_django_logging(self) -> bool:
        return self.integration.use_django_logging

    @property
    def log_parent(self) -> bool:
        return self.integration.log_parent

    def validate(self) -> None:
        if not isinstance(self.use_django_logging, bool):
            raise ImproperlyConfigured('The CeleryIntegration use_django_logging setting must be a boolean.')
        if not isinstance(self.log_parent, bool):
            raise ImproperlyConfigured('The CeleryIntegration log_parent setting must be a boolean.')
