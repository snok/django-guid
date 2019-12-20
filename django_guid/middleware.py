import logging
import threading
import uuid
from typing import Union

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


class GuidMiddleware(object):
    """
    Injects a GUID into the thread that is accessible from anywhere in the Django app
    """

    _guid = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> Union[HttpRequest, HttpResponse]:
        """
        Fetches the current thread from the pool and stores the GUID to that thread, making it
        accessible through this class.
        Also handles deletion of that thread after the request is done.
        :param request: HttpRequest from Django
        :return: Passes on the Request or Response to the next middleware
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
        Fetches the GUID to the current thread, or the optionally
        provided default if there is no current GUID.
        :return: Fetches the GUID for the thread
        """
        return cls._guid.get(threading.current_thread(), default)

    @classmethod
    def set_guid(cls, guid):
        """
        Sets the GUID to the thread
        :param guid: A guid/uuid4
        """
        cls._guid[threading.current_thread()] = guid

    @classmethod
    def del_guid(cls):
        """
        Delete the guid that was stored for the current thread.
        """
        cls._guid.pop(threading.current_thread(), None)

    @staticmethod
    def _generate_guid() -> str:
        """
        Generates an UUIDv4/GUID as a string
        :return: GUID
        """
        return uuid.uuid4().hex

    @staticmethod
    def _validate_guid(original_guid: str) -> bool:
        try:
            guid_value = uuid.UUID(original_guid, version=4)
        except ValueError:
            return False
        return original_guid == guid_value.hex

    def _get_correlation_id_from_header(self, request: HttpRequest) -> str:
        """
        Returns either the provided GUID or a new one, depending on if it's a valid GUID or not.
        :param request: HttpRequest object
        :return: guid
        """
        given_guid = str(request.headers.get('Correlation-ID'))
        if self._validate_guid(given_guid):
            return given_guid
        return self._generate_guid()

    def _get_id_from_header(self, request: HttpRequest) -> str:
        logger.info(request.headers)
        if request.headers.get('Correlation-ID'):  # Case insensitive headers.get added in Django2.2 so this is safe
            logger.info(f"Header found {request.headers.get('Correlation-ID')}")
            request.correlation_id = self._get_correlation_id_from_header(request)
        else:
            request.correlation_id = self._generate_guid()
            logger.info(f'No Correlation-ID found in the header. Added correlation id: {request.correlation_id}')
        return request.correlation_id
