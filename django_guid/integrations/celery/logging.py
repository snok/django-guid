from typing import Any

from celery.signals import setup_logging


@setup_logging.connect
def config_loggers(*args: Any, **kwargs: Any) -> None:  # pragma: no cover
    """
    Configures celery to use the Django settings.py logging configuration.
    """
    from logging.config import dictConfig

    from django.conf import settings

    dictConfig(settings.LOGGING)
