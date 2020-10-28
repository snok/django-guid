API
===

Getting started
---------------
You can either use the ``contextvar``  directly by importing it with ``django_guid.middleware import guid``,
or use the API which also logs changes. If you want to use the contextvar, please see the official Python docs.

To use the API import the functions you'd like to use:

.. code-block:: python

    from django_guid import get_guid, set_guid, clear_guid


get_guid()
----------
* **Returns**: ``str`` or ``None``, if set by Django-GUID.

Fetches the GUID.

.. code-block:: python

    guid = get_guid()

set_guid()
----------
* **Parameters**: ``guid``: ``str``

Sets the GUID to the given input.

.. code-block:: python

    set_guid('My GUID')


clear_guid()
------------
Clears the guid (sets it to ``None``)

.. code-block:: python

    clear_guid()


Example usage
-------------

.. code-block:: python

    import requests
    from django.conf import settings

    from django_guid import get_guid

    requests.get(
        url='http://localhost/api',
        headers={
            'Accept': 'application/json',
            settings.DJANGO_GUID['GUID_HEADER_NAME']: get_guid(),
        }
    )
