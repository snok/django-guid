import logging

from django_guid.integrations import Integration

logger = logging.getLogger('django_guid')


class CeleryIntegration(Integration):
    """
    Forwards correlation IDs to Celery workers when a task is published from
    a request, and generates unique correlation IDs for all other tasks.
    """

    identifier = 'CeleryIntegration'

    def __init__(self, use_django_logging: bool = False, log_parent: bool = False) -> None:
        """
        :param use_django_logging: If true, configures Celery to use the logging settings defined in settings.py
        :param log_parent: If true, traces the origin of a task. Needs to be True to use the celery referral log filter.
        """
        super().__init__()
        self.log_parent = log_parent
        self.use_django_logging = use_django_logging

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
