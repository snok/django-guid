import pytest
from django.core.exceptions import ImproperlyConfigured


def test_missing_identifier(monkeypatch):
    """
    Tests that an exception is raised when identifier is missing.
    """
    from django_guid.integrations.sentry import SentryIntegration

    monkeypatch.setattr(SentryIntegration, 'identifier', None)
    with pytest.raises(ImproperlyConfigured, match='`identifier` cannot be None'):
        SentryIntegration()


def test_missing_run_method(monkeypatch, client):
    """
    Tests that an exception is raised when the run method has not been defined.
    """
    from django_guid.config import settings as guid_settings
    from django_guid.integrations.sentry import SentryIntegration

    monkeypatch.delattr(SentryIntegration, 'run')
    monkeypatch.setattr(guid_settings, 'INTEGRATIONS', [SentryIntegration()])
    with pytest.raises(ImproperlyConfigured, match='The integration `Sentry` is missing a `run` method'):
        client.get('/api')
