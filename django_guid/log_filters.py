from logging import Filter
from typing import TYPE_CHECKING

from django_guid.context import guid

if TYPE_CHECKING:
    from logging import LogRecord


class CorrelationId(Filter):
    def __init__(self, correlation_id_field: str = 'correlation_id') -> None:
        super().__init__()
        self.correlation_id_field = correlation_id_field

    def filter(self, record: 'LogRecord') -> bool:
        """
        Add the correlation ID to the log record.
        :param record: Log record
        :param correlation_id_field: record field on which the correlation id is set
        :return: True
        """
        setattr(record, self.correlation_id_field, guid.get())
        return True
