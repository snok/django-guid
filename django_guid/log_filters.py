import logging

from django_guid_injection.middleware import GuidInjection


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
        record.correlation_id = GuidInjection.get_guid()
        return True
