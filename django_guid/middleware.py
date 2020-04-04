import logging
import threading
import uuid
from typing import Callable, Union

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest, HttpResponse

from django_guid.config import settings

logger = logging.getLogger('django_guid')


class GuidMiddleware(object):
    """
    Gets a GUID from a request header, or generates a GUID if none is found, for each incoming request.
    Stored GUIDs are accessible from anywhere in the Django app.
    """

    _guid = {}

    def __init__(self, get_response: Callable) -> None:
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response

        # This logic cannot be moved to config.py because apps are not yet initialized when that is executed
        if not apps.is_installed('django_guid'):
            raise ImproperlyConfigured('django_guid must be in installed apps')

    def __call__(self, request: HttpRequest) -> Union[HttpRequest, HttpResponse]:
        """
        Fetches the current thread ID from the pool and stores the GUID in the _guid class variable,
        with the thread ID as the key.

        Deletes the GUID from the object unless settings are overwritten.

        :param request: HttpRequest from Django
        :return: Passes on the request or response to the next middleware
        """
        if request.get_full_path().strip('/') in settings.IGNORE_URLS:
            return self.get_response(request)

        # Process request and store the GUID on the thread
        self.set_guid(self._get_id_from_header(request))

        # Run all integrations
        for integration in settings.INTEGRATIONS:
            logger.debug('Running integration: `%s`', integration.identifier)
            integration.run(guid=self.get_guid())

        # ^ Code above this line is executed before the view and later middleware
        response = self.get_response(request)

        if settings.RETURN_HEADER:
            response[settings.GUID_HEADER_NAME] = self.get_guid()  # Adds the GUID to the response header
            if settings.EXPOSE_HEADER:
                response['Access-Control-Expose-Headers'] = settings.GUID_HEADER_NAME

        # Run tear down for all the integrations
        for integration in settings.INTEGRATIONS:
            logger.debug('Running tear down for integration: `%s`', integration.identifier)
            integration.cleanup()

        return response

    @classmethod
    def get_guid(cls, default: str = None) -> str:
        """
        Fetches the GUID of the current thread from _guid.
        If no value has been set for the current thread yet, a default value is returned.

        :param default: Optional value to return if no GUID has been set on the current thread.
        :return: GUID or default.
        """
        return cls._guid.get(threading.current_thread(), default)

    @classmethod
    def set_guid(cls, guid: str) -> None:
        """
        Assigns a GUID to the thread.

        :param guid: The GUID being assigned
        :return: None
        """
        cls._guid[threading.current_thread()] = guid

    @classmethod
    def delete_guid(cls) -> None:
        """
        Delete the thread's GUID.

        :return: None
        """
        guid = cls.get_guid()
        if guid:
            logger.debug('Deleting %s from _guid', guid)
            cls._guid.pop(threading.current_thread(), None)

    @staticmethod
    def _generate_guid() -> str:
        """
        Generates an UUIDv4/GUID as a string.

        :return: GUID
        """
        return uuid.uuid4().hex

    @staticmethod
    def _validate_guid(original_guid: str) -> bool:
        """
        Validates a GUID.

        :param original_guid: string to validate
        :return: bool
        """
        try:
            return bool(uuid.UUID(original_guid, version=4).hex)
        except ValueError:
            logger.warning('Failed to validate GUID %s', original_guid)
            return False

    def _get_correlation_id_from_header(self, request: HttpRequest) -> str:
        """
        Returns either the provided GUID or a new one depending on if the provided GUID is valid or not.

        :param request: HttpRequest object
        :return: GUID
        """
        given_guid = str(request.headers.get(settings.GUID_HEADER_NAME))
        if not settings.VALIDATE_GUID:
            logger.debug('Returning ID from header without validating it as a GUID')
            return given_guid
        elif settings.VALIDATE_GUID and self._validate_guid(given_guid):
            logger.debug('%s is a valid GUID', given_guid)
            return given_guid
        else:
            new_guid = self._generate_guid()
            logger.info('%s is not a valid GUID. New GUID is %s', given_guid, new_guid)
            return new_guid

    def _get_id_from_header(self, request: HttpRequest) -> str:
        """
        Checks if the request contains the header specified in the Django settings.
        If it does, we fetch the header and attempt to validate the contents as GUID.
        If no header is found, we generate a GUID to be injected instead.

        :param request: HttpRequest object
        :return: GUID
        """
        header = request.headers.get(settings.GUID_HEADER_NAME)  # Case insensitive headers.get added in Django2.2
        if header:
            logger.info('%s found in the header: %s', settings.GUID_HEADER_NAME, header)
            request.correlation_id = self._get_correlation_id_from_header(request)
        else:
            request.correlation_id = self._generate_guid()
            logger.info(
                'Header `%s` was not found in the incoming request. Generated new GUID: %s',
                settings.GUID_HEADER_NAME,
                request.correlation_id,
            )
        return request.correlation_id
