import pytest
from django.core.exceptions import ImproperlyConfigured


def test_different_header_guids(client, monkeypatch, caplog):
    """
    Tests that the package handles multiple header values by defaulting to one and logging a warning.
    """
    from django_guid.integrations import SentryIntegration
    from django_guid.config import settings as guid_settings

    monkeypatch.setattr(guid_settings, 'INTEGRATIONS', [SentryIntegration()])
    client.get(
        '/api', **{'HTTP_Correlation-ID': '97c304252fd14b25b72d6aee31565842',},
    )
