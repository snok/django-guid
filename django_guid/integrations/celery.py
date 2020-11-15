import logging

from django_guid.integrations import Integration

logger = logging.getLogger('django_guid')


class CeleryIntegration(Integration):
    """
    Ensures that our correlation ID is transferred to Celery workers when
    we publish tasks from a request, or generates an ID when published by Celery beat.
    """

    identifier = 'CeleryIntegration'

    def __init__(self, use_django_logging: bool = False, log_origin: bool = False) -> None:
        super().__init__()
        self.log_origin = log_origin
        self.use_django_logging = use_django_logging

    def setup(self) -> None:
        """
        Loads Celery signals.
        """
        from django_guid.celery.signals import before_task_publish, task_postrun, task_prerun  # noqa

        if self.use_django_logging:
            from django_guid.celery.logging import config_loggers  # noqa

    def run(self, guid: str, **kwargs) -> None:
        """
        Does nothing.
        """
        pass
