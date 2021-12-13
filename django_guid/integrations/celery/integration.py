import logging
from typing import Any

from django_guid.integrations import Integration

logger = logging.getLogger('django_guid')


class CeleryIntegration(Integration):
    """
    Passes correlation IDs from parent processes to child processes in a Celery context.

    This means a correlation ID can be transferred from a request to a worker, or from a worker to another worker.

    For workers executing scheduled tasks, a correlation ID is generated for each new task.
    """

    identifier = 'CeleryIntegration'

    def __init__(
        self,
        use_django_logging: bool = False,
        log_parent: bool = False,
        uuid_length: int = 32,
        sentry_integration: bool = False,
    ) -> None:
        """
        :param use_django_logging: If true, configures Celery to use the logging settings defined in settings.py
        :param log_parent: If true, traces the origin of a task. Should be True if you wish to use the CeleryTracing log filter.
        :param uuid_length: Optionally lets you set the length of the celery IDs generated for the log filter
        """
        super().__init__()
        self.log_parent = log_parent
        self.use_django_logging = use_django_logging
        self.uuid_length = uuid_length
        self.sentry_integration = sentry_integration

    def setup(self) -> None:
        """
        Loads Celery signals.
        """
        # Import pre-configured Celery signals that will pass on the correlation ID to a celery worker
        # or will generate a correlation ID when a worker starts a scheduled task
        from django_guid.integrations.celery.signals import before_task_publish, task_postrun, task_prerun  # noqa

        if self.use_django_logging:
            # Import pre-configured Celery signals that makes Celery adopt the settings.py log config
            from django_guid.integrations.celery.logging import config_loggers  # noqa

    def run(self, guid: str, **kwargs: Any) -> None:
        """
        Does nothing, as all we need for Celery tracing is to register signals during setup.
        """
        pass  # pragma: no cover
