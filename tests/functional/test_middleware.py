from unittest.mock import patch
from django.test import override_settings


@patch('django_guid.middleware.uuid.uuid4')
def test_request_with_no_correlation_id(mock_uuid, client, caplog):
    """
    Tests a request without any correlation-ID in it logs the correct things.
    In this case, it means that the first log message should not have any correlation-ID in it, but the next two
    (from views and services.useless_file) should have.
    :param mock_uuid: uuid4 patch
    :param client: Django client
    :param caplog: caplog fixture
    """
    mock_uuid.return_value.hex = '704ae5472cae4f8daa8f2cc5a5a8mock'
    client.get('/')
    assert [None, '704ae5472cae4f8daa8f2cc5a5a8mock',
            '704ae5472cae4f8daa8f2cc5a5a8mock'] == [x.correlation_id for x in caplog.records]


def test_request_with_correlation_id(client, caplog):
    """
    Tests a request _with_ a correlation-ID in it logs the correct things.
    :param client: Django client
    :param caplog: caplog fixture
    """
    client.get('/', **{'HTTP_Correlation-ID': '97c304252fd14b25b72d6aee31565843'})
    assert [None,  # log message about finding a GUID
            None,  # log message that confirms that the GUID has been validated
            '97c304252fd14b25b72d6aee31565843',  # view and function should log the correlation ID we provided
            '97c304252fd14b25b72d6aee31565843'] == [x.correlation_id for x in caplog.records]


@patch('django_guid.middleware.uuid.uuid4')
def test_request_with_invalid_correlation_id(mock_uuid, client, caplog):
    """
    Tests that a request with an invalid GUID is replaced when VALIDATE_GUID is True.
    :param client: Django client
    :param caplog: Caplog fixture
    """
    mock_uuid.return_value.hex = '704ae5472cae4f8daa8f2cc5a5a8mock'

    client.get('/', **{'HTTP_Correlation-ID': 'bad-guid'})
    assert [None,  # log message about finding a GUID
            None,  # log message that confirms that the GUID is not validated.
            '704ae5472cae4f8daa8f2cc5a5a8mock',  # Should have a new generated UUID and not bad-guid
            '704ae5472cae4f8daa8f2cc5a5a8mock'] == [x.correlation_id for x in caplog.records]


def test_request_with_invalid_correlation_id_without_validation(client, caplog, settings):
    """
    Tests that a request with an invalid GUID is replaced when VALIDATE_GUID is False.
    :param client: Django client
    :param caplog: Caplog fixture
    :param settings: Django settings fixture
    """
    settings.DJANGO_GUID = {'GUID_HEADER_NAME': 'Correlation-IIID', 'VALIDATE_GUID': True}
    client.get('/', **{'HTTP_Correlation-ID': 'bad-guid'})
    assert [None,  # log message about finding a GUID
            None,  # log message that confirms that the GUID is not to be validated.
            'bad-guid',  # Should have bad-guid, as we do not generate new ones
            'bad-guid'] == [x.correlation_id for x in caplog.records]
