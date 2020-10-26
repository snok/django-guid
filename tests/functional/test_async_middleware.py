import asyncio


async def test_one_request(async_client, caplog, mock_uuid):
    response = await async_client.get('/asgi')
    expected = [
        ('async middleware called', None),
        (
            'Header `Correlation-ID` was not found in the incoming request. Generated '
            'new GUID: 704ae5472cae4f8daa8f2cc5a5a8mock',
            None,
        ),
        ('This log message should have a GUID', '704ae5472cae4f8daa8f2cc5a5a8mock'),
        ('Going to sleep for a sec', '704ae5472cae4f8daa8f2cc5a5a8mock'),
        ('Going to sleep for a sec', '704ae5472cae4f8daa8f2cc5a5a8mock'),
        ('Warning, I am awake!', '704ae5472cae4f8daa8f2cc5a5a8mock'),
        ('Warning, I am awake!', '704ae5472cae4f8daa8f2cc5a5a8mock'),
        ('Received signal `request_finished`, clearing guid', '704ae5472cae4f8daa8f2cc5a5a8mock'),
    ]

    assert [(x.message, x.correlation_id) for x in caplog.records] == expected
    assert response['Correlation-ID'] == '704ae5472cae4f8daa8f2cc5a5a8mock'


async def test_two_requests_concurrently(async_client, caplog, mock_uuid_two_unique, two_unique_uuid4):
    """
    Checks that a following request does not inherit a previous GUID
    """
    tasks = [asyncio.create_task(async_client.get('/asgi')), asyncio.create_task(async_client.get('/asgi'))]
    await asyncio.gather(*tasks)
    expected = [
        t
        for guid in two_unique_uuid4
        for t in [
            ('async middleware called', None),
            (
                f'Header `Correlation-ID` was not found in the incoming request. Generated new GUID: {guid}',
                None,
            ),
            ('This log message should have a GUID', guid),
            ('Going to sleep for a sec', guid),
            ('Going to sleep for a sec', guid),
            ('Warning, I am awake!', guid),
            ('Warning, I am awake!', guid),
            ('Received signal `request_finished`, clearing guid', guid),
        ]
    ]
    # Sort both lists and compare - order will vary between runs
    assert sorted([(x.message, x.correlation_id) for x in caplog.records]) == sorted(expected)


async def test_ignored_url(async_client, caplog, monkeypatch):
    """
    Test that a URL specified in IGNORE_URLS is ignored in the async view
    :param async_client: Django async client
    :param caplog: Caplog fixture
    :param monkeypatch: Monkeypatch for django settings
    """
    from django_guid.config import settings as guid_settings

    monkeypatch.setattr(guid_settings, 'IGNORE_URLS', {'no-guid'})  # Same as it would be after config conversion
    await async_client.get('/no-guid')
    # No log message should have a GUID, aka `None` on index 1.
    expected = [
        ('async middleware called', None),
        ('This log message should NOT have a GUID - the URL is in IGNORE_URLS', None),
        ('Some warning in a function', None),
        ('Received signal `request_finished`, clearing guid', None),
    ]
    assert [(x.message, x.correlation_id) for x in caplog.records] == expected
