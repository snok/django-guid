import logging

from django_guid.context import guid

logger = logging.getLogger('django_guid')


def get_guid() -> str:
    """
    Fetches the GUID of the current request
    """
    return guid.get()


def set_guid(new_guid: str) -> str:
    """
    Assigns a GUID to the current request
    """
    old_guid = guid.get()
    if old_guid:
        logger.info('Changing the guid ContextVar from %s to %s', old_guid, new_guid)
    guid.set(new_guid)
    return new_guid


def clear_guid() -> None:
    """
    Clears the GUID of the current request
    """
    old_guid = guid.get()
    if old_guid:
        logger.info('Clearing %s from the guid ContextVar', old_guid)
    guid.set(None)
