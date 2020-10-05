import logging
import asyncio

logger = logging.getLogger(__name__)


async def useless_function() -> bool:
    """
    Useless function to demonstrate a function log message.
    :return: True
    """
    logger.info('Going to sleep for a sec')
    await asyncio.sleep(10)

    logger.warning('Warning, I am awake!')
    return True
