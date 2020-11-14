from __future__ import absolute_import, unicode_literals

import logging
import os
import uuid

from celery import Celery
from celery.signals import setup_logging, before_task_publish, task_prerun

logger = logging.getLogger(__name__)

if os.name == 'nt':
    # Windows configuration to make celery run ok on Windows
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demoproj.settings')

app = Celery('django_guid')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@setup_logging.connect
def config_loggers(*args, **kwargs):
    """
    Configures celery to use the Django settings.py logging configuration.
    """
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)


@before_task_publish.connect
def before_celery_task_handler(headers, **kwargs):
    from django_guid import get_guid
    logger.debug('Before task handler')
    if guid := get_guid():
        logger.info('Setting GUID header value')
        headers['HTTP_X_REQUEST_ID'] = guid


@task_prerun.connect
def prerun_celery_task_handler(task, **kwargs):
    """
    TODO: Verify description
    Sets the GUID of the current thread based on the request ID found in
    the task received.
    """
    from django_guid import set_guid, get_guid
    logger.debug('Pre-run handler')

    if heroku_request_id := task.request.get('HTTP_X_REQUEST_ID', None):
        logger.info('Found header ID, setting GUID based on that')
        set_guid(heroku_request_id)
    elif guid := get_guid():
        logger.debug(f'A GUID already exists ({guid})')
    else:
        logger.info(f'Setting guid')
        set_guid(str(uuid.uuid4()))


# -----------------------------------------

@app.task(bind=True)
def debug_task(self):
    """
    This is just an example task.
    """
    logger.info('test')
    second_debug_task.delay()


@app.task(bind=True)
def second_debug_task(self):
    """
    This is just an example task.
    """
    logger.info('test 2')
