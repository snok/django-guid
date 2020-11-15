from logging import Filter, LogRecord

from django_guid.celery.context import celery


class CeleryReferralId(Filter):
    def filter(self, record: LogRecord) -> bool:
        """
        Sets a celery-referrer log filter to show which process spawned the current process.

        The format of the filter is [{referrer} -> {current}] and looks like [5b883 -> 14c33]
        """
        record.celery_referrer: str = celery.get()  # type: ignore
        return True
