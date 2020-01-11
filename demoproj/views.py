import logging

from django.http import HttpRequest, JsonResponse

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
    return JsonResponse({'Detail': f'It worked! Useless function response is {useless_response}'})
