import logging
import os

from celery import Celery

logger = logging.getLogger(__name__)

if os.name == 'nt':
    # Windows configuration to make celery run ok on Windows
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demoproj.settings')

app = Celery('django_guid')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task()
def debug_task() -> None:
    """
    This is just an example task.
    """
    logger.info('Debug task 1')
    second_debug_task.delay()
    second_debug_task.delay()


@app.task()
def second_debug_task() -> None:
    """
    This is just an example task.
    """
    logger.info('Debug task 2')
    third_debug_task.delay()
    fourth_debug_task.delay()


@app.task()
def third_debug_task() -> None:
    """
    This is just an example task.
    """
    logger.info('Debug task 3')
    fourth_debug_task.delay()
    fourth_debug_task.delay()


@app.task()
def fourth_debug_task() -> None:
    """
    This is just an example task.
    """
    logger.info('Debug task 4')
