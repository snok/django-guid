import logging
import threading
import uuid
from typing import Union

from django.http import HttpRequest, HttpResponse

from django_guid.config import settings

logger = logging.getLogger(__name__)


class GuidMiddleware(object):
    """
    Checks for an existing GUID (correlation ID) in a request's headers.
    If a header value is found, the value is validated as a GUID and stored, before the request is passed to the next middleware.
    If no value is found, or one is found but is invalid, we generate and store a new GUID on the thread.
    Stored GUIDs are accessible from anywhere in the Django app.
    """

    _guid = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> Union[HttpRequest, HttpResponse]:
        """
        Fetches the current thread from the pool and stores the GUID to that thread,
        making it accessible via this class.
        Also handles deletion of that thread after the request is done.
        :param request: HttpRequest from Django
        :return: Passes on the request or response to the next middleware
        """
        # Process request and store the GUID on the thread
        self.set_guid(self._get_id_from_header(request))
        # ^ Code above this line is executed before the view and later middleware
        response = self.get_response(request)
        # Delete the current request to avoid memory leak
        self.__class__.del_guid()
        return response

    @classmethod
    def get_guid(cls, default=None):
        """
        Fetches the GUID of the current thread, from _guid.
        If no value has been set for the current thread yet, we return a default value.
        :default: Optional value to return if no GUID has been set on the current thread.
        :return: GUID or default.
        """
        return cls._guid.get(threading.current_thread(), default)

    @classmethod
    def set_guid(cls, guid: str) -> None:
        """
        Assigns a GUID to the thread.
        :param guid: str
        :return: None
        """
        cls._guid[threading.current_thread()] = guid

    @classmethod
    def del_guid(cls) -> None:
        """
        Delete the guid that was stored for the current thread.
        :return: None
        """
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
            return original_guid == uuid.UUID(original_guid, version=4).hex
        except ValueError:
            return False

    def _get_correlation_id_from_header(self, request: HttpRequest) -> str:
        """
        Returns either the provided GUID or a new one,
        depending on if the provided GUID is valid, and the specified settings
        :param request: HttpRequest object
        :return: GUID
        """
        given_guid = str(request.headers.get(settings.GUID_HEADER_NAME))
        if not settings.VALIDATE_GUID:
            return given_guid
        elif settings.VALIDATE_GUID and self._validate_guid(given_guid):
            return given_guid
        else:
            return self._generate_guid()

    def _get_id_from_header(self, request: HttpRequest) -> str:
        """
        Checks if the request contains the header specified in the Django settings.
        If it does, we fetch the header and attempt to validate the contents as GUID.
        If no header is found, we generate a GUID to be injected instead.
        :param request: HttpRequest object
        :return: GUID
        """
        guid_header_name = settings.GUID_HEADER_NAME

        if request.headers.get(guid_header_name):  # Case insensitive headers.get added in Django2.2 so this is safe
            logger.info(f'{guid_header_name} found in the header: {request.headers.get(guid_header_name)}')
            request.correlation_id = self._get_correlation_id_from_header(request)
        else:
            request.correlation_id = self._generate_guid()
            logger.info(f'No {guid_header_name} found in the header. Added {guid_header_name}: {request.correlation_id}')

        return request.correlation_id
