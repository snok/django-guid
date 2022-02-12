import asyncio
import logging
from typing import Callable, Union

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

from django_guid.context import guid
from django_guid.utils import get_id_from_header, ignored_url

try:
    from django.utils.decorators import sync_and_async_middleware
except ImportError:  # pragma: no cover
    raise ImproperlyConfigured('Please use Django GUID 2.x for Django>=3.1. (`pip install django-guid>3`).')

from typing import TYPE_CHECKING

from django_guid.config import settings

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

logger = logging.getLogger('django_guid')


def process_incoming_request(request: 'HttpRequest') -> None:
    """
    Processes an incoming request. This function is called before the view and later middleware.
    Same logic for both async and sync views.
    """
    if not ignored_url(request=request):
        # Process request and store the GUID in a contextvar
        guid.set(get_id_from_header(request))

        # Run all integrations
        for integration in settings.integrations:
            logger.debug('Running integration: `%s`', integration.identifier)
            integration.run(guid=guid.get())


def process_outgoing_request(response: 'HttpResponse', request: 'HttpRequest') -> None:
    """
    Process an outgoing request. This function is called after the view and before later middleware.
    """
    if not ignored_url(request=request):
        if settings.return_header:
            response[settings.guid_header_name] = guid.get()  # Adds the GUID to the response header
            if settings.expose_header:
                response['Access-Control-Expose-Headers'] = settings.guid_header_name

        # Run tear down for all the integrations
        for integration in settings.integrations:
            logger.debug('Running tear down for integration: `%s`', integration.identifier)
            integration.cleanup()


@sync_and_async_middleware
def guid_middleware(get_response: Callable) -> Callable:
    """
    Add this middleware to the top of your middlewares.
    """
    # One-time configuration and initialization.
    if not apps.is_installed('django_guid'):
        raise ImproperlyConfigured('django_guid must be in installed apps')
    # fmt: off
    if asyncio.iscoroutinefunction(get_response):
        async def middleware(request: 'HttpRequest') -> Union['HttpRequest', 'HttpResponse']:
            logger.debug('async middleware called')
            process_incoming_request(request=request)
            # ^ Code above this line is executed before the view and later middleware
            response = await get_response(request)
            process_outgoing_request(response=response, request=request)
            return response
    else:
        def middleware(request: 'HttpRequest') -> Union['HttpRequest', 'HttpResponse']:  # type: ignore
            logger.debug('sync middleware called')
            process_incoming_request(request=request)
            # ^ Code above this line is executed before the view and later middleware
            response = get_response(request)
            process_outgoing_request(response=response, request=request)
            return response
    # fmt: on
    return middleware
