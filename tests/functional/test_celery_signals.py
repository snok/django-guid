
def test_request_with_no_correlation_id(client, caplog):
    response = client.get('/celery')
