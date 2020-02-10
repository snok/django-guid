Settings
========

.. _skip_cleanup_setting:

SKIP_CLEANUP
------------
* **Default**: ``False``
* **Type**: ``boolean``

After the request is done, the GUID is deleted to avoid memory leaks. Memory leaks can happen in the
case of many threads, or especially when using Gunicorn :code:`max_requests` or similar settings,
where the number of thread IDs can potentially scale for ever.
Having clean up enabled ensures we can not have memory leaks, but comes at the cost that anything that happens
after this middleware will not have the GUID attached, such as :code:`django.request` or :code:`django.server`
logs. If you do not want clean up of GUIDs and know what you're doing, you can enable :code:`SKIP_CLEANUP`.


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
