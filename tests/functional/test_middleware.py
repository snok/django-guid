import pytest


@pytest.fixture
def mock_uuid(monkeypatch):
    class MockUUid:
        hex = '704ae5472cae4f8daa8f2cc5a5a8mock'

    monkeypatch.setattr('django_guid.middleware.uuid.uuid4', MockUUid)


def test_request_with_no_correlation_id(client, caplog, mock_uuid):
    """
    Tests a request without any correlation-ID in it logs the correct things.
    In this case, it means that the first log message should not have any correlation-ID in it, but the next two
    (from views and services.useless_file) should have.
    :param mock_uuid: Monkeypatch fixture for mocking UUID
    :param client: Django client
    :param caplog: caplog fixture
    """
    client.get('/')
    expected = [
        ('No Correlation-ID found in the header. Added Correlation-ID: 704ae5472cae4f8daa8f2cc5a5a8mock', None),
        ('This log message should have a GUID', '704ae5472cae4f8daa8f2cc5a5a8mock'),
        ('Some warning in a function', '704ae5472cae4f8daa8f2cc5a5a8mock'),
        ('Deleting 704ae5472cae4f8daa8f2cc5a5a8mock from _guid', '704ae5472cae4f8daa8f2cc5a5a8mock')]
    assert [(x.message, x.correlation_id) for x in caplog.records] == expected


def test_request_with_correlation_id(client, caplog):
    """
    Tests a request _with_ a correlation-ID in it logs the correct things.
    :param client: Django client
    :param caplog: caplog fixture
    """
    client.get('/', **{'HTTP_Correlation-ID': '97c304252fd14b25b72d6aee31565843'})
    expected = [('Correlation-ID found in the header: 97c304252fd14b25b72d6aee31565843', None),
                ('97c304252fd14b25b72d6aee31565843 is a valid GUID', None),
                ('This log message should have a GUID', '97c304252fd14b25b72d6aee31565843'),
                ('Some warning in a function', '97c304252fd14b25b72d6aee31565843'),
                ('Deleting 97c304252fd14b25b72d6aee31565843 from _guid', '97c304252fd14b25b72d6aee31565843')]
    assert [(x.message, x.correlation_id) for x in caplog.records] == expected


def test_request_with_invalid_correlation_id(client, caplog, mock_uuid):
    """
    Tests that a request with an invalid GUID is replaced when VALIDATE_GUID is True.
    :param client: Django client
    :param caplog: Caplog fixture
    :param mock_uuid: Monkeypatch fixture for mocking UUID
    """
    client.get('/', **{'HTTP_Correlation-ID': 'bad-guid'})
    expected = [
        ('Correlation-ID found in the header: bad-guid', None),
        ('bad-guid is not a valid GUID. New GUID is 704ae5472cae4f8daa8f2cc5a5a8mock', None),
        ('This log message should have a GUID', '704ae5472cae4f8daa8f2cc5a5a8mock'),
        ('Some warning in a function', '704ae5472cae4f8daa8f2cc5a5a8mock'),
        ('Deleting 704ae5472cae4f8daa8f2cc5a5a8mock from _guid', '704ae5472cae4f8daa8f2cc5a5a8mock')
    ]
    assert [(x.message, x.correlation_id) for x in caplog.records] == expected


def test_request_with_invalid_correlation_id_without_validation(client, caplog, monkeypatch):
    """
    Tests that a request with an invalid GUID is replaced when VALIDATE_GUID is False.
    :param client: Django client
    :param caplog: Caplog fixture
    :param monkeypatch: Monkeypatch for django settings
    """
    from django_guid.config import settings as guid_settings
    monkeypatch.setattr(guid_settings, 'VALIDATE_GUID', False)
    client.get('/', **{'HTTP_Correlation-ID': 'bad-guid'})
    expected = [
        ('Correlation-ID found in the header: bad-guid', None),
        ('VALIDATE_GUID is not True, will not validate given GUID', None),
        ('This log message should have a GUID', 'bad-guid'),
        ('Some warning in a function', 'bad-guid'),
        ('Deleting bad-guid from _guid', 'bad-guid')
    ]
    assert [(x.message, x.correlation_id) for x in caplog.records] == expected


def test_request_with_skip_cleanup(client, caplog, monkeypatch, mock_uuid):
    """
    Tests that a request skips cleanup if SKIP_CLEANUP is True
    :param client: Django client
    :param caplog: Caplog fixture
    :param monkeypatch: Monkeypatch for django settings
    """
    from django_guid.config import settings as guid_settings
    monkeypatch.setattr(guid_settings, 'SKIP_CLEANUP', True)
    monkeypatch.setattr(guid_settings, 'VALIDATE_GUID', False)
    client.get('/', **{'HTTP_Correlation-ID': 'bad-guid'})
    client.get('/', **{'HTTP_Correlation-ID': 'another-bad-guid'})
    expected = [
        # First request
        ('Correlation-ID found in the header: bad-guid', None),
        ('VALIDATE_GUID is not True, will not validate given GUID', None),
        ('This log message should have a GUID', 'bad-guid'),
        ('Some warning in a function', 'bad-guid'),
        ('Deleting bad-guid from _guid', 'bad-guid'),
        # Second request
        ('Correlation-ID found in the header: another-bad-guid', None),
        ('VALIDATE_GUID is not True, will not validate given GUID', None),
        ('This log message should have a GUID', 'another-bad-guid'),
        ('Some warning in a function', 'another-bad-guid')
    ]
    assert [(x.message, x.correlation_id) for x in caplog.records] == expected
