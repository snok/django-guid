from celery.signals import setup_logging


@setup_logging.connect
def config_loggers(*args, **kwargs) -> None:  # noqa: ANN002
    """
    Configures celery to use the Django settings.py logging configuration.
    """
    from logging.config import dictConfig

    from django.conf import settings

    dictConfig(settings.LOGGING)
