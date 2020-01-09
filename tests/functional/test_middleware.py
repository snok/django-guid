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
    expected = [None,
                '704ae5472cae4f8daa8f2cc5a5a8mock',
                '704ae5472cae4f8daa8f2cc5a5a8mock']
    assert [x.correlation_id for x in caplog.records] == expected


def test_request_with_correlation_id(client, caplog):
    """
    Tests a request _with_ a correlation-ID in it logs the correct things.
    :param client: Django client
    :param caplog: caplog fixture
    """
    client.get('/', **{'HTTP_Correlation-ID': '97c304252fd14b25b72d6aee31565843'})
    expected = [None,  # log message about finding a GUID
                None,  # log message that confirms that the GUID has been validated
                '97c304252fd14b25b72d6aee31565843',  # view and function should log the correlation ID we provided
                '97c304252fd14b25b72d6aee31565843']
    assert [x.correlation_id for x in caplog.records] == expected


def test_request_with_invalid_correlation_id(client, caplog, mock_uuid):
    """
    Tests that a request with an invalid GUID is replaced when VALIDATE_GUID is True.
    :param client: Django client
    :param caplog: Caplog fixture
    :param mock_uuid: Monkeypatch fixture for mocking UUID
    """
    client.get('/', **{'HTTP_Correlation-ID': 'bad-guid'})
    expected = [None,  # log message about finding a GUID
                None,  # log message that confirms that the GUID is not validated.
                '704ae5472cae4f8daa8f2cc5a5a8mock',  # Should have a new generated UUID and not bad-guid
                '704ae5472cae4f8daa8f2cc5a5a8mock']
    assert [x.correlation_id for x in caplog.records] == expected


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
    expected = [None,  # log message about finding a GUID
                None,  # log message that confirms that the GUID is not to be validated.
                'bad-guid',  # Should have bad-guid, as we do not generate new ones
                'bad-guid']
    assert [x.correlation_id for x in caplog.records] == expected
