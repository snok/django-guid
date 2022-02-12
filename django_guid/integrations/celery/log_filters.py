from logging import Filter
from typing import TYPE_CHECKING

from django_guid.integrations.celery.context import celery_current, celery_parent

if TYPE_CHECKING:
    from logging import LogRecord


class CeleryTracing(Filter):
    # noinspection PyTypeHints
    def filter(self, record: 'LogRecord') -> bool:
        """
        Sets two record attributes: celery parent and celery current.
        Celery origin is the tracing ID of the process that spawned the current
        process, and celery current is the current process' tracing ID.

        In other words, if a worker sent a task to be executed by the worker pool,
        that celery worker's `current` tracing ID would become the next worker's `origin` tracing ID.
        """
        record.celery_parent_id: str = celery_parent.get()  # type: ignore
        record.celery_current_id: str = celery_current.get()  # type: ignore
        return True
