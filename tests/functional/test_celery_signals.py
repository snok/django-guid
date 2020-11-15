# import time
#
#
# def test_celery(client, caplog):
#     from celery.utils.log import get_task_logger
#
#     response = client.get('/celery')
#     for message in caplog.records:
#         print(message.message)
#     time.sleep(1)
#     print(get_task_logger.__dict__)
