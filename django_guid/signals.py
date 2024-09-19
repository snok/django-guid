import logging
from typing import Any, Optional

from django.core.signals import request_finished
from django.dispatch import receiver

from django_guid.context import guid

logger = logging.getLogger('django_guid')


@receiver(request_finished)
def clear_guid(sender: Optional[dict], **kwargs: Any) -> None:
    """
    Receiver function for when a request finishes.

    When a request is finished, clear the GUID from the contextvar. This ensures a GUID is never passed down to
    the next request in sync views.

    :param sender: The sender of the signal. By documentation, we must allow this input parameter.
    :param kwargs: The request_finished signal does not actually send any kwargs, but Django will throw an error
        if we don't accept them. This is because at any point arguments could get added to the signal, and the receiver
        must be able to handle those new arguments.
    :return: None
    """
    logger.debug('Received signal `request_finished`, clearing guid')
    guid.set(None)
