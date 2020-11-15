import logging

from django_guid.integrations import Integration

logger = logging.getLogger('django_guid')


class CeleryIntegration(Integration):
    """
    Passes correlation IDs from parent processes to child processes in a Celery context.

    This means a correlation ID can be transferred from a request to a worker, or
    from a worker to another worker. For workers executing scheduled tasks,
    a correlation ID is set for each task.
    """

    identifier = 'CeleryIntegration'

    def __init__(self, use_django_logging: bool = False, log_parent: bool = False, uuid_length: int = 32) -> None:
        """
        :param use_django_logging: If true, configures Celery to use the logging settings defined in settings.py
        :param log_parent: If true, traces the origin of a task. Should be True if you wish to use the CeleryParentId log filter.
        """
        super().__init__()
        self.log_parent = log_parent
        self.use_django_logging = use_django_logging
        self.uuid_length = uuid_length

    def setup(self) -> None:
        """
        Loads Celery signals.
        """
        from django_guid.integrations.celery.signals import before_task_publish, task_postrun, task_prerun  # noqa

        if self.use_django_logging:
            from django_guid.integrations.celery.logging import config_loggers  # noqa

    def run(self, guid: str, **kwargs) -> None:
        """
        Does nothing, as all we need for Celery tracing is to register signals during setup.
        """
        pass
