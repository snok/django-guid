import logging

from celery.signals import before_task_publish, task_postrun, task_prerun

from django_guid import clear_guid, get_guid, set_guid
from django_guid.config import settings
from django_guid.integrations.celery.context import celery_current, celery_parent
from django_guid.utils import generate_guid

logger = logging.getLogger('django_guid.celery')


@before_task_publish.connect
def _before_task_publish(headers: dict, **kwargs) -> None:
    """
    Called when a request or celery worker publishes a task to the worker pool
    by calling task.delay(), task.apply_async() or using another equivalent method.

    This is where we transfer state from a parent process to a child process.
    """
    guid = get_guid()
    logger.info('Setting task request header', guid)
    headers[settings.guid_header_name] = guid

    if settings.integration_settings.celery.log_parent:
        current = celery_current.get()
        if current:
            headers['CELERY_PARENT_ID'] = current


@task_prerun.connect
def _task_prerun(task, **kwargs) -> None:  # noqa: ANN001
    """
    Called before a worker starts executing a task.

    Here we make sure to set the appropriate correlation ID for all logs logged
    during the tasks, and on the thread in general. In that regard, this does
    the Celery equivalent to what the django-guid middleware does for a request.
    """
    guid = task.request.get(settings.guid_header_name, None)
    if guid:
        logger.info('Setting GUID %s', guid)
        set_guid(guid)
    else:
        generated_guid = generate_guid()
        logger.info('Generated GUID %s', generated_guid)
        set_guid(generated_guid)

    if settings.integration_settings.celery.log_parent:
        origin = task.request.get('CELERY_PARENT_ID')
        if origin:
            logger.info('Setting parent ID %s', origin)
            celery_parent.set(origin)
            generated_current_guid = generate_guid()
            logger.info('Generated current ID %s', generated_current_guid)
            celery_current.set(generated_current_guid)


@task_postrun.connect
def _task_postrun(task, **kwargs) -> None:  # noqa: ANN001
    """
    Called after a task is finished.

    Here we make sure to clean up the IDs we set in the pre-run method, so that
    the next task executed by the same worker doesn't inherit the same IDs.
    """
    logger.debug('Cleaning up GUIDs')
    clear_guid()

    if settings.integration_settings.celery.log_parent:
        celery_current.set(None)
        celery_parent.set(None)
