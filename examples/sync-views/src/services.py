import logging

logger = logging.getLogger(__name__)


def some_sync_function() -> None:
    logger.info('Doing some work')
