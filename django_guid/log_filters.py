import logging

from django_guid.middleware import GuidMiddleware


class CorrelationId(logging.Filter):

    def filter(self, record) -> bool:
        """
        Determines that the specified record is to be logged.

        From the docs:
                Is the specified record to be logged? Returns 0 for no, nonzero for
                yes. If deemed appropriate, the record may be modified in-place.
        :param record: Log record
        :return: True
        """
        record.correlation_id = GuidMiddleware.get_guid()
        return True
