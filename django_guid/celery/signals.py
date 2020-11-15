import logging

from celery.signals import before_task_publish, task_postrun, task_prerun
from django_guid import clear_guid, get_guid, set_guid
from django_guid.celery.context import celery
from django_guid.config import settings
from django_guid.utils import generate_guid

logger = logging.getLogger('django_guid')


@before_task_publish.connect
def _before_task_publish(headers: dict, **kwargs) -> None:
    """
    Called when a task is published using task.delay()

    Setting the correct header here means we can correctly trace a request
    that spawns background workers.
    """
    if guid := get_guid():
        # A GUID will exist when the current thread was spawned for a request
        # or by another task.
        logger.info('Setting task request header using existing GUID (%s)', guid)
    else:
        # No GUID will exist when a task is published by Celery beat.
        guid = generate_guid()
        set_guid(guid)
        logger.info('Setting task request header using generated GUID (%s)', guid)

    # Set correlation ID in the task header for the worker to read.
    headers[settings.GUID_HEADER_NAME] = guid

    """
    Logic above this comment makes sure we're able to trace all logs generated from a request,
    even when the request spawns background workers.

    This is sufficient for most projects, but what happens if we run task.delay() three times in a row?
    You would probably see something like this

    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] -- Message 1
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] -- Message 2
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] -- Message 1
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] -- Message 2
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] -- Message 1
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] -- Message 2

    Three sets of identical logs will be logged with the same exact tracing ID, which is better than no tracing ID,
    but not good ideal. So in addition to the tracing ID, the logic below this comment attempts to add some information
    about what process is currently running, so we can take use that information in the task_prerun signal to add depth to our logs.

    The general idea is that we can then use an additional log filter for depth.

    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [1-2] -- Message 1
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [1-2] -- Message 2
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [1-3] -- Message 1
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [1-3] -- Message 2
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [1-4] -- Message 1
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [1-4] -- Message 2

    and if each of these processes spawned subprocesses, it might look like this

    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [1-2] -- Message 1
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [1-2] -- Message 2
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [1-3] -- Message 1
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [1-3] -- Message 2
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [1-4] -- Message 1
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [1-4] -- Message 2
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [2-5] -- Message 3
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [3-6] -- Message 3
    %(level)s %(time)s [c061ce714cb147068e2fdcc572ae820b] [4-7] -- Message 3

    and so on...

    Most likely you wouldn't want this in your console output, but it could
    be very useful to include as extra data.

    The [origin-current] filter also cannot be as simple as [1-2], because
    we don't have shared state between all processes, only between one
    process to the next, that means sibling processes don't know they exists.
    We therefore double down on uuids and create this format: [cdfba -> e65de]
    """
    if settings.INTEGRATION_SETTINGS.celery.log_origin:
        short_guid = generate_guid()[:5]
        # ^ decided to use a shortened uuid to represent origin
        # If string representations of uuids can be 0-9, a-f, A-F, then there
        # are 9 + 6 + 6 = 21 possible characters that could be generated.
        # Unless I'm doing this wrong, that should mean the likelihood of a colliding 5-character uuid
        # should be 1/21 ** 5 which is 0,0000244851927, or 1 in 4,084,101
        # that seems fine for this use case - if you're reading this and find this
        # unacceptably low, just submit a PR, and I'm sure we can revise it.

        if not (origin := celery.get()):
            # This means we're a request sending a task to a worker
            headers['CELERY_ORIGIN'] = f'{short_guid}'
        else:
            # If we're in this block, it means we're a worker
            if ' -> ' not in origin:
                # This means we're 1 step down
                headers['CELERY_ORIGIN'] = f'{origin} -> {short_guid}'
            else:
                # This means we're 2+ steps down the chain
                headers['CELERY_ORIGIN'] = f'{origin.split(" -> ")[1]} -> {short_guid}'


@task_prerun.connect
def _task_prerun(task, **kwargs) -> None:  # noqa: ANN001
    """
    Called before executing a worker executes a task.

    Set the GUID for a task from the task request header if it exists,
    and generates a GUID if not. In that regard, this is
    the Celery equivalent of the django-guid middleware.
    """
    if guid := task.request.get(settings.GUID_HEADER_NAME, None):
        logger.info('Setting GUID for celery worker from header')
        set_guid(guid)
    else:
        logger.info('Generating GUID for celery worker')
        set_guid(generate_guid())

    if settings.INTEGRATION_SETTINGS.celery.log_origin:
        if origin := task.request.get('CELERY_ORIGIN'):
            celery.set(origin)


@task_postrun.connect
def _task_postrun(task, **kwargs) -> None:  # noqa: ANN001
    """
    Called after a task has been executed.

    Clears the GUID for the worker thread.
    """
    logger.debug('Clearing GUID for celery worker')
    clear_guid()
    if settings.INTEGRATION_SETTINGS.celery.log_origin:
        celery.set(None)
