from __future__ import absolute_import, unicode_literals

import logging
import os
import uuid

from celery import Celery
from celery.signals import setup_logging, before_task_publish, task_prerun, \
    task_postrun

from django_guid import set_guid

logger = logging.getLogger('django_guid')

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

# -----------------------------------------

@app.task(bind=True)
def debug_task(self):
    """
    This is just an example task.
    """
    logger.info('Debug task 1')
    second_debug_task.delay()


@app.task(bind=True)
def second_debug_task(self):
    """
    This is just an example task.
    """
    logger.info('Debug task 2')
    third_debug_task.delay()


@app.task(bind=True)
def third_debug_task(self):
    """
    This is just an example task.
    """
    logger.info('Debug task 2')
    raise Exception('test')
