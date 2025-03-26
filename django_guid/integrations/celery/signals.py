import logging
from typing import TYPE_CHECKING, Any

from celery.signals import before_task_publish, task_postrun, task_prerun

from django_guid import clear_guid, get_guid, set_guid
from django_guid.config import settings
from django_guid.integrations.celery.context import celery_current, celery_parent
from django_guid.utils import generate_guid

if TYPE_CHECKING:
    from celery import Task

logger = logging.getLogger('django_guid.celery')

parent_header = 'CELERY_PARENT_ID'


def set_transaction_id(guid: str) -> None:
    """
    Sets the Sentry transaction ID if the Celery sentry integration setting is True.
    """
    if settings.integration_settings.celery.sentry_integration:
        import sentry_sdk
        from packaging import version

        if version.parse(sentry_sdk.VERSION) >= version.parse('2.12.0'):
            with sentry_sdk.isolation_scope() as scope:
                scope.set_tag('transaction_id', guid)
        else:
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag('transaction_id', guid)

        logger.debug('Setting Sentry transaction_id to %s', guid)


@before_task_publish.connect
def publish_task_from_worker_or_request(headers: dict, **kwargs: Any) -> None:
    """
    Called when a request or celery worker publishes a task to the worker pool
    by calling task.delay(), task.apply_async() or using another equivalent method.
    This is where we transfer state from a parent process to a child process.
    """
    guid = get_guid()
    logger.info('Setting task request header as %s', guid)
    headers[settings.guid_header_name] = guid

    if settings.integration_settings.celery.log_parent:
        current = celery_current.get()
        if current:
            headers[parent_header] = current


@task_prerun.connect
def worker_prerun(task: 'Task', **kwargs: Any) -> None:
    """
    Called before a worker starts executing a task.
    Here we make sure to set the appropriate correlation ID for all logs logged
    during the tasks, and on the thread in general. In that regard, this does
    the Celery equivalent to what the django-guid middleware does for a request.
    """
    guid = task.request.get(settings.guid_header_name)
    if guid:
        logger.info('Setting GUID %s', guid)
        set_guid(guid)
        set_transaction_id(guid)
    else:
        generated_guid = generate_guid(uuid_length=settings.integration_settings.celery.uuid_length)
        logger.info('Generated GUID %s', generated_guid)
        set_guid(generated_guid)
        set_transaction_id(generated_guid)

    if settings.integration_settings.celery.log_parent:
        origin = task.request.get(parent_header)
        if origin:
            logger.info('Setting parent ID %s', origin)
            celery_parent.set(origin)
        generated_current_guid = generate_guid(uuid_length=settings.integration_settings.celery.uuid_length)
        logger.info('Generated current ID %s', generated_current_guid)
        celery_current.set(generated_current_guid)


@task_postrun.connect
def clean_up(task: 'Task', **kwargs: Any) -> None:
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
