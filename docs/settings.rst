Settings
========

Package settings are added in your ``settings.py``:

Default settings are shown below:

.. code-block:: python

    DJANGO_GUID = {
        'GUID_HEADER_NAME': 'Correlation-ID',
        'VALIDATE_GUID': True,
        'RETURN_HEADER': True,
        'EXPOSE_HEADER': True,
        'INTEGRATIONS': [],
        'UUID_LENGTH': 32,
        'UUID_FORMAT': 'hex',
    }



.. _guid_header_name_setting:

GUID_HEADER_NAME
----------------
* **Default**: ``Correlation-ID``
* **Type**: ``string``

The name of the GUID to look for in a header in an incoming request. Remember that it's case insensitive.

.. _validate_guid_setting:

VALIDATE_GUID
-------------
* **Default**: ``True``
* **Type**: ``boolean``


Whether the :code:`GUID_HEADER_NAME` should be validated or not.
If the GUID sent to through the header is not a valid GUID (:code:`uuid.uuid4`).


RETURN_HEADER
-------------
* **Default**: ``True``
* **Type**: ``boolean``

Whether to return the GUID (Correlation-ID) as a header in the response or not.
It will have the same name as the :code:`GUID_HEADER_NAME` setting.


EXPOSE_HEADER
-------------
* **Default**: ``True``
* **Type**: ``boolean``

Whether to return :code:`Access-Control-Expose-Headers` for the GUID header if
:code:`RETURN_HEADER` is :code:`True`, has no effect if :code:`RETURN_HEADER` is :code:`False`.
This is allows the JavaScript Fetch API to access the header when CORS is enabled.

INTEGRATIONS
------------
* **Default**: ``[]``
* **Type**: ``list``

Whether to enable any custom or available integrations with :code:`django_guid`.
As an example, using :code:`SentryIntegration()` as an integration would set Sentry's :code:`transaction_id` to
match the GUID used by the middleware.

IGNORE_URLS
-----------
* **Default**: ``[]``
* **Type**: ``list``

URL endpoints where the middleware will be disabled. You can put your health check endpoints here.

UUID_LENGTH
-----------
* **Default**: ``36``
* **Type**: ``int``

If a full UUID hex is too long for you, this settings lets you specify the length you wish to use.
The chance of collision in a UUID is so low, that most systems will get away with a lot
fewer than 32 characters.

UUID_LENGTH
-----------
* **Default**: ``hex``
* **Type**: ``string``

If a UUID hex is not suitable for you, this settings lets you specify the format you wish to use. The options are:
* ``hex``: The default, a 32 character hexadecimal string. e.g. ee586b0fba3c44849d20e1548210c050
* ``str``: A 36 character string. e.g. ee586b0f-ba3c-4484-9d20-e1548210c050
