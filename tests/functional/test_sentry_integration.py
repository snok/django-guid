import pytest
from django.core.exceptions import ImproperlyConfigured


def test_sentry_integration(client, monkeypatch, caplog, mocker):
    """
    Tests the sentry integration
    """
    from sentry_sdk.scope import Scope
    from django_guid.integrations import SentryIntegration
    from django_guid.config import settings as guid_settings

    monkeypatch.setattr(guid_settings, 'INTEGRATIONS', [SentryIntegration()])
    mock_scope = mocker.patch.object(Scope, 'set_tag')

    client.get('/api', **{'HTTP_Correlation-ID': '97c304252fd14b25b72d6aee31565842'})
    expected = [
        (None, 'Correlation-ID found in the header: 97c304252fd14b25b72d6aee31565842'),
        (None, '97c304252fd14b25b72d6aee31565842 is a valid GUID'),
        ('97c304252fd14b25b72d6aee31565842', 'Running integration: `SentryIntegration`'),
        ('97c304252fd14b25b72d6aee31565842', 'Setting Sentry transaction_id to 97c304252fd14b25b72d6aee31565842'),
        ('97c304252fd14b25b72d6aee31565842', 'This is a DRF view log, and should have a GUID.'),
        ('97c304252fd14b25b72d6aee31565842', 'Some warning in a function'),
        ('97c304252fd14b25b72d6aee31565842', 'Running tear down for integration: `SentryIntegration`'),
        ('97c304252fd14b25b72d6aee31565842', 'Received signal `request_finished`'),
        ('97c304252fd14b25b72d6aee31565842', 'Deleting 97c304252fd14b25b72d6aee31565842 from _guid'),
    ]
    mock_scope.assert_called_with('transaction_id', '97c304252fd14b25b72d6aee31565842')
    assert [(x.correlation_id, x.message) for x in caplog.records] == expected


def test_sentry_validation(client, monkeypatch):
    """
    Tests that the package handles multiple header values by defaulting to one and logging a warning.
    """
    import sys
    from django_guid.integrations import SentryIntegration
    from django_guid.config import Settings
    from django.conf import settings

    # Mock away the sentry_sdk dependency
    sys.modules['sentry_sdk'] = None

    monkeypatch.setattr(settings, 'DJANGO_GUID', {'INTEGRATIONS': [SentryIntegration()]})
    with pytest.raises(
        ImproperlyConfigured,
        match='The package `sentry-sdk` is required for extending your tracing IDs to Sentry. '
        'Please run `pip install sentry-sdk` if you wish to include this integration.',
    ):
        Settings()
