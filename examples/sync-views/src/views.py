import logging
from typing import TYPE_CHECKING

from django.http import JsonResponse

from django_guid.context import guid
from .services import some_sync_function

if TYPE_CHECKING:
    from django.http import HttpRequest

logger = logging.getLogger(__name__)


def index_view(request: 'HttpRequest') -> JsonResponse:
    logger.info('This log message should have a correlation ID')
    some_sync_function()
    return JsonResponse({'correlationId': f'{guid.get()}'})
