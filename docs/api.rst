API
===

Getting started
---------------
To use the API import the ``guid``:

.. code-block:: python

    from django_guid.middleware import guid


get()
----------
* **Returns**: ``str`` or ``None``

Fetches the GUID.

.. code-block:: python

    guid = guid.get()

set()
----------
* **Parameters**: ``guid``: ``str``

Sets the GUID to the given input. If you want to delete the current GUID, set it to ``None``.

.. code-block:: python

    guid.set('My GUID')


Example usage
-------------

.. code-block:: python

    import requests
    from django.conf import settings

    from django_guid.middleware import guid

    requests.get(
        url='http://localhost/api',
        headers={
            'Accept': 'application/json',
            settings.DJANGO_GUID['GUID_HEADER_NAME']: guid.get(),
        }
    )
