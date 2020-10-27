import pytest


@pytest.mark.asyncio
async def test_api(async_client, caplog, mock_uuid):
    await async_client.get('/api-usage')
    expected = [
        ('async middleware called', None),
        (
            'Header `Correlation-ID` was not found in the incoming request. Generated '
            'new GUID: 704ae5472cae4f8daa8f2cc5a5a8mock',
            None,
        ),
        ('Current GUID: 704ae5472cae4f8daa8f2cc5a5a8mock', '704ae5472cae4f8daa8f2cc5a5a8mock'),
        (
            'Changing the guid ContextVar from 704ae5472cae4f8daa8f2cc5a5a8mock to ' 'another guid',
            '704ae5472cae4f8daa8f2cc5a5a8mock',
        ),
        ('Current GUID: another guid', 'another guid'),
        ('Clearing another guid from the guid ContextVar', 'another guid'),
        ('Current GUID: None', None),
        ('Received signal `request_finished`, clearing guid', None),
    ]
    assert [(x.message, x.correlation_id) for x in caplog.records] == expected
