import logging
from typing import TYPE_CHECKING

from django.http import JsonResponse

from django_guid.context import guid
from .services import some_sync_function

if TYPE_CHECKING:
    from django.http import HttpRequest

logger = logging.getLogger(__name__)


def ignored_view(request: 'HttpRequest') -> JsonResponse:
    logger.info('This log message should NOT have a correlation ID - the URL is in IGNORE_URLS')
    some_sync_function()
    return JsonResponse({'correlationId': f'{guid.get()}'})
