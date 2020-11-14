from __future__ import absolute_import, unicode_literals

import logging

from django_guid.integrations import Integration

logger = logging.getLogger('django_guid')


class CeleryIntegration(Integration):
    """
    Ensures that our correlation ID is transferred to Celery workers when
    we publish tasks from a request, or generates an ID when published by Celery beat.
    """

    identifier = 'CeleryIntegration'

    def setup(self) -> None:
        """
        Loads Celery signals.
        """
        from django_guid.celery.signals import task_prerun, task_postrun, before_task_publish  # noqa

    def run(self, guid: str, **kwargs) -> None:
        pass
