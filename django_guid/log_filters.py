from logging import Filter
from typing import TYPE_CHECKING

from django_guid.middleware import guid

if TYPE_CHECKING:
    from logging import LogRecord


class CorrelationId(Filter):
    def filter(self, record: 'LogRecord') -> bool:
        """
        Determines that the specified record is to be logged.

        From the docs:
                Is the specified record to be logged? Returns 0 for no, nonzero for
                yes. If deemed appropriate, the record may be modified in-place.
        :param record: Log record
        :return: True
        """
        record.correlation_id = guid.get()  # type: ignore[attr-defined]
        return True
