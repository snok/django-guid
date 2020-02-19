import logging
from typing import Optional

from django.core.signals import request_finished
from django.dispatch import receiver

from .middleware import GuidMiddleware

logger = logging.getLogger('django_guid')


@receiver(request_finished)
def delete_guid(sender: Optional[dict], **kwargs: dict) -> None:
    """
    Receiver function for when a request finishes.

    When a request is finished, delete a requests _guid reference to prevent memory leaks.

    :param sender: dict or None
    :param kwargs: dict
    :return: None
    """
    logger.debug('Received signal `request_finished`')
    GuidMiddleware.delete_guid()
