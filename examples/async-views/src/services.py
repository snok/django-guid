import asyncio
import logging
from random import randint

logger = logging.getLogger(__name__)


async def some_async_function() -> int:
    logger.info('Doing i/o bound work')
    await asyncio.sleep(1)
    logger.warning('Finished i/o bound work')
    return randint(0, 10)
