import asyncio
import logging
import threading
import uuid
from contextvars import ContextVar
from typing import Callable, Union

from asgiref.local import Local
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest, HttpResponse

from django_guid.config import settings

logger = logging.getLogger('django_guid')


def generate_guid() -> str:
    """
    Generates an UUIDv4/GUID as a string.

    :return: GUID
    """
    return uuid.uuid4().hex


def validate_guid(original_guid: str) -> bool:
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
