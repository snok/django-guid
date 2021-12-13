import sys

from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

import pytest
from sentry_sdk.scope import Scope

from django_guid.config import Settings
from django_guid.integrations import SentryIntegration

mocked_settings = {
    'GUID_HEADER_NAME': 'Correlation-ID',
    'VALIDATE_GUID': True,
    'INTEGRATIONS': [SentryIntegration()],
    'IGNORE_URLS': ['no-guid'],
}


def test_sentry_integration(client, caplog, mocker, monkeypatch):
    """
    Tests the sentry integration
    """
    mock_scope = mocker.patch.object(Scope, 'set_tag')
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.middleware.settings', settings)
        client.get('/api', **{'HTTP_Correlation-ID': '97c304252fd14b25b72d6aee31565842'})
        expected = [
            (None, 'sync middleware called'),
            (None, 'Correlation-ID found in the header'),
            (None, '97c304252fd14b25b72d6aee31565842 is a valid GUID'),
            ('97c304252fd14b25b72d6aee31565842', 'Running integration: `SentryIntegration`'),
            ('97c304252fd14b25b72d6aee31565842', 'Setting Sentry transaction_id to 97c304252fd14b25b72d6aee31565842'),
            ('97c304252fd14b25b72d6aee31565842', 'This is a DRF view log, and should have a GUID.'),
            ('97c304252fd14b25b72d6aee31565842', 'Some warning in a function'),
            ('97c304252fd14b25b72d6aee31565842', 'Running tear down for integration: `SentryIntegration`'),
            ('97c304252fd14b25b72d6aee31565842', 'Received signal `request_finished`, clearing guid'),
        ]
        mock_scope.assert_called_with('transaction_id', '97c304252fd14b25b72d6aee31565842')
        assert [(x.correlation_id, x.message) for x in caplog.records] == expected


def test_sentry_validation(client):
    """
    Tests that the package handles multiple header values by defaulting to one and logging a warning.
    """

    # Mock away the sentry_sdk dependency
    backup = None
    if 'sentry_sdk' in sys.modules:
        backup = sys.modules['sentry_sdk']
        sys.modules['sentry_sdk'] = None

    with override_settings(DJANGO_GUID=mocked_settings):
        with pytest.raises(
            ImproperlyConfigured,
            match='The package `sentry-sdk` is required for extending your tracing IDs to Sentry. '
            'Please run `pip install sentry-sdk` if you wish to include this integration.',
        ):
            Settings().validate()

    # Put it back in - otherwise a bunch of downstream tests break
    if backup:
        sys.modules['sentry_sdk'] = backup
