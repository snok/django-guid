API
===

Getting started
---------------
To use the API import the GuidMiddleware:

.. code-block:: python

    from django_guid.middleware import GuidMiddleware


get_guid()
----------
* **Parameters**: ``default`` = ``None`` - What to return if no ``GUID`` is found.

* **Returns**: ``str`` or ``default``

Fetches the GUID.

.. code-block:: python

    guid = GuidMiddleware.get_guid(default=None)

set_guid()
----------
* **Parameters**: ``guid``: ``str``

Sets the GUID to the given input

.. code-block:: python

    GuidMiddleware.set_guid('My GUID')


delete_guid()
-------------
Deletes the stored GUID

.. code-block:: python

    GuidMiddleware.delete_guid()


Example usage
-------------

.. code-block:: python

    import requests
    from django.conf import settings

    from django_guid.middleware import GuidMiddleware

    requests.get(
        url='http://localhost/api',
        headers={
            'Accept': 'application/json',
            settings.DJANGO_GUID['GUID_HEADER_NAME']: GuidMiddleware.get_guid(),
        }
    )
