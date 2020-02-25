import logging
from typing import Optional

from django.core.signals import request_finished
from django.dispatch import receiver

from django_guid.middleware import GuidMiddleware

logger = logging.getLogger('django_guid')


@receiver(request_finished)
def delete_guid(sender: Optional[dict], **kwargs: dict) -> None:
    """
    Receiver function for when a request finishes.

    When a request is finished, delete a requests _guid reference to prevent memory leaks.

    :param sender: The sender of the signal. By documentation, we must allow this input parameter.
    :param kwargs: The request_finished signal does not actually send any kwargs, but Django will throw an error 
        if we don't accept them. This is because at any point arguments could get added to the signal, and the reciever
        must be able to handle those new arguments.
    :return: None
    """
    logger.debug('Received signal `request_finished`')
    GuidMiddleware.delete_guid()
