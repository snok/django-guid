from django.core.exceptions import ImproperlyConfigured

import pytest

from django_guid.integrations.celery import CeleryIntegration
from django_guid.integrations.celery.config import CeleryIntegrationSettings


def test_validate_use_django_logging():
    """
    Test that validation for use_django_logging works as expected
    """
    invalid_settings = [{}, [], 'asd', -1, 0, 3.3]
    valid_settings = [True, False]
    for setting in invalid_settings:
        with pytest.raises(
            ImproperlyConfigured, match='The CeleryIntegration use_django_logging setting must be a boolean.'
        ):
            CeleryIntegrationSettings(CeleryIntegration(use_django_logging=setting))

    for setting in valid_settings:
        CeleryIntegrationSettings(CeleryIntegration(use_django_logging=setting))


def test_validate_log_parent():
    """
    Test that validation logic for log_parent works as expected
    """
    invalid_settings = [{}, [], 'asd', -1, 0, 3.3]
    valid_settings = [True, False]
    for setting in invalid_settings:
        with pytest.raises(ImproperlyConfigured, match='The CeleryIntegration log_parent setting must be a boolean.'):
            CeleryIntegrationSettings(CeleryIntegration(log_parent=setting))

    for setting in valid_settings:
        CeleryIntegrationSettings(CeleryIntegration(log_parent=setting))


def test_validate_uuid_length():
    """
    Test that validation for uuid_length works as expected
    """
    invalid_settings = [True, False, {}, [], 'asd', -1, 0, 3.3, 33]
    valid_settings = [1, 15, 32]
    for setting in invalid_settings:
        with pytest.raises(ImproperlyConfigured, match='The CeleryIntegration uuid_length setting must be an integer.'):
            CeleryIntegrationSettings(CeleryIntegration(uuid_length=setting))

    for setting in valid_settings:
        CeleryIntegrationSettings(CeleryIntegration(uuid_length=setting))
