from typing import Optional

from django.core.signals import request_finished
from django.dispatch import receiver

from .middleware import GuidMiddleware


@receiver(request_finished)
def delete_guid(sender: Optional[dict], **kwargs: dict) -> None:
    """
    Receiver function for when a request finishes.
    When a request is finished,
    we make sure that the current requests _guid reference is deleted to prevent a memory leak.

    :param sender: dict or None
    :param kwargs: dict
    :return: None
    """
    GuidMiddleware.delete_guid()
