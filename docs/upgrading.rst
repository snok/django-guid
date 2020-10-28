.. _upgrading:

************************************
Upgrading Django-GUID 2.x.x to 3.x.x
************************************

Upgrading to ``Django>=3.1.1`` and using async/ASGI requires you to use ``Django-GUID`` version 3 or higher.

In order to upgrade, you need to do the following:

1. Change Middleware
--------------------

* **From:** ``django_guid.middleware.GuidMiddleware``
* **To:** ``django_guid.middleware.guid_middleware``


.. code-block:: python

    MIDDLEWARE = [
        'django_guid.middleware.guid_middleware',
        ...
     ]


2. Change API functions (if you used them)
------------------------------------------

**From:**


.. code-block:: python

    from django_guid.middleware import GuidMiddleware
    GuidMiddleware.get_guid()
    GuidMiddleware.set_guid('x')
    GuidMiddleware.delete_guid()



**To:**


.. code-block:: python

    from django_guid import clear_guid, get_guid, set_guid
    get_guid()
    set_guid('x')
    clear_guid()  # Note the name change from delete to clear
