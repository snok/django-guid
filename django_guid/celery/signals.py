from __future__ import absolute_import, unicode_literals

import logging
import uuid

from celery.signals import before_task_publish, task_prerun, \
    task_postrun

from django_guid import set_guid

logger = logging.getLogger('django_guid')


@before_task_publish.connect
def before_task_publish(headers, **kwargs):
    """
    Called when a task is published using task.delay()

    Setting the correct header here means we can correctly trace a request
    that spawns background workers.
    """
    from django_guid import get_guid

    if guid := get_guid():
        logger.info(
            'Setting task request header using existing GUID (%s)',
            guid)
    else:
        set_guid(uuid.uuid4().hex)
        logger.info(
            'Setting task request header using generated GUID (%s)',
            get_guid())

    # This adds a header for the worker to read
    headers['Correlation-ID'] = guid


@task_prerun.connect
def task_prerun(task, **kwargs):
    """
    Called before executing a worker executes a task.

    Set the GUID for a task from the task request header if it exists,
    and generates a GUID if not. In that regard, this is
    the Celery equivalent of the django-guid middleware.
    """
    from django_guid import set_guid

    if guid := task.request.get('Correlation-ID', None):
        logger.info('Setting GUID for celery worker from header')
        set_guid(guid)
    else:
        logger.info(f'Generating GUID for celery worker')
        set_guid(uuid.uuid4().hex)


@task_postrun.connect
def task_postrun(task, **kwargs):
    """
    Called after a task has been executed.

    Clears the GUID for the worker thread.
    """
    from django_guid import clear_guid

    logger.debug('Clearing GUID for celery worker')
    clear_guid()
