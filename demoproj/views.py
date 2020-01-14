import logging

from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from demoproj.services.useless_file import useless_function

logger = logging.getLogger(__name__)


def index_view(request: HttpRequest) -> JsonResponse:
    """
    Example view that logs a log and calls a function that logs a log.

    :param request: HttpRequest
    :return: JsonResponse
    """
    logger.info('This log message should have a GUID')
    useless_response = useless_function()
    return JsonResponse({'detail': f'It worked! Useless function response is {useless_response}'})


@api_view(('GET',))
def rest_view(request: Request) -> Response:
    """
    Example DRF view that logs a log and calls a function that logs a log.

    :param request: Request
    :return: Response
    """
    logger.info('This is a DRF view log, and should have a GUID.')
    useless_response = useless_function()
    return Response(data={'detail': f'It worked! Useless function response is {useless_response}'})
