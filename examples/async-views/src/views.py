import asyncio
import logging
from typing import TYPE_CHECKING

from django.http import JsonResponse

from .services import some_async_function

if TYPE_CHECKING:
    from django.http import HttpRequest

logger = logging.getLogger(__name__)


async def index_view(request: 'HttpRequest') -> JsonResponse:
    logger.info('Fetching counts asynchronously')
    counts = await asyncio.gather(
        asyncio.create_task(some_async_function()), asyncio.create_task(some_async_function())
    )
    return JsonResponse({'sum': sum(counts)})
