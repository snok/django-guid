import logging
import asyncio
from django.http import JsonResponse

from demoproj.services.async_services import useless_function
from django_guid import get_guid, set_guid, clear_guid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest

logger = logging.getLogger(__name__)


async def index_view(request: 'HttpRequest') -> JsonResponse:
    """
    Example view that logs a log and calls a function that logs a log.

    :param request: HttpRequest
    :return: JsonResponse
    """
    logger.info('This log message should have a GUID')
    task_one = asyncio.create_task(useless_function())
    task_two = asyncio.create_task(useless_function())
    results = await asyncio.gather(task_one, task_two)
    return JsonResponse({'detail': f'It worked! Useless function response is {results}'})


async def django_guid_api_usage(request: 'HttpRequest') -> JsonResponse:
    """
    Uses each API function
    """
    logger.info('Current GUID: %s', get_guid())
    set_guid('another guid')
    logger.info('Current GUID: %s', get_guid())
    clear_guid()
    logger.info('Current GUID: %s', get_guid())
    return JsonResponse({'detail': ':)'})
