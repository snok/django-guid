###########
Django GUID
###########

.. image:: https://img.shields.io/pypi/v/django-guid.svg
    :target: https://pypi.python.org/pypi/django-guid
.. image:: https://img.shields.io/pypi/pyversions/django-guid.svg
    :target: https://pypi.python.org/pypi/django-guid#downloads
.. image:: https://img.shields.io/pypi/djversions/django-guid.svg
    :target: https://pypi.python.org/pypi/django-guid
.. image:: https://codecov.io/gh/jonasks/django-guid/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jonasks/django-guid
.. image:: https://readthedocs.org/projects/django-guid/badge/?version=latest
    :target: https://django-guid.readthedocs.io/en/latest/?badge=latest
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://django-guid.readthedocs.io/en/latest/?badge=latest


Django GUID attaches a unique correlation ID to all your log outputs for every requests you handle. Since every error now has an ID tying connecting it to all other relevant logs,
this makes debugging your application easy.

Further integration is also possible, as the ID can be returned as a header, or you can include it as a header in outgoing requests, to extend the reach of IDs to whole systems.

**Resources**:

* Documentation: https://django-guid.readthedocs.io
* Homepage: https://github.com/JonasKs/django-guid
* Free software: BSD License

**Examples**

Log output with a GUID:

.. code-block::

    INFO ... [0d1c3919e46e4cd2b2f4ac9a187a8ea1] project.views This is a DRF view log, and should have a GUID.
    INFO ... [99d44111e9174c5a9494275aa7f28858] project.views This is a DRF view log, and should have a GUID.
    WARNING ... [0d1c3919e46e4cd2b2f4ac9a187a8ea1] project.services.file Some warning in a function
    WARNING ... [99d44111e9174c5a9494275aa7f28858] project.services.file Some warning in a function

Log output without a GUID:

.. code-block::

    INFO ... project.views This is a DRF view log, and should have a GUID.
    INFO ... project.views This is a DRF view log, and should have a GUID.
    WARNING ... project.services.file Some warning in a function
    WARNING ... project.services.file Some warning in a function



************
Installation
************

Install using pip:

    pip install django-guid


********
Settings
********

Package settings are added in your :code:`settings.py`.

Example:

.. code-block:: python

    DJANGO_GUID = {
        GUID_HEADER_NAME = 'Correlation-ID',
        VALIDATE_GUID = True,
        RETURN_HEADER = True,
        EXPOSE_HEADER = True,
        SKIP_CLEANUP = False,
    }

Details:

* :code:`GUID_HEADER_NAME`
        The name of the GUID to look for in a header in an incoming request. Remember that it's case insensitive.

    Default: Correlation-ID

* :code:`VALIDATE_GUID`
        Whether the :code:`GUID_HEADER_NAME` should be validated or not.
        If the GUID sent to through the header is not a valid GUID (:code:`uuid.uuid4`).

    Default: True

* :code:`RETURN_HEADER`
        Whether to return the GUID (Correlation-ID) as a header in the response or not.
        It will have the same name as the :code:`GUID_HEADER_NAME` setting.

    Default: True

* :code:`EXPOSE_HEADER`
        Whether to return :code:`Access-Control-Expose-Headers` for the GUID header if
        :code:`RETURN_HEADER` is :code:`True`, has no effect if :code:`RETURN_HEADER` is :code:`False`.
        This is allows the JavaScript Fetch API to access the header when CORS is enabled.

    Default: True

* :code:`SKIP_CLEANUP`
        After the request is done, the GUID is deleted to avoid memory leaks. Memory leaks can happen in the
        case of many threads, or especially when using Gunicorn :code:`max_requests` or similar settings,
        where the number of thread IDs can potentially scale for ever.
        Having clean up enabled ensures we can not have memory leaks, but comes at the cost that anything that happens
        after this middleware will not have the GUID attached, such as :code:`django.request` or :code:`django.server`
        logs. If you do not want clean up of GUIDs and know what you're doing, you can enable :code:`SKIP_CLEANUP`.

    Default: False

*************
Configuration
*************

Once settings have been added, in your project's :code:`settings.py` you need to do the following:

1. Middleware
=============

Add the :code:`django_guid.middleware.GuidMiddleware` to your ``MIDDLEWARE``:

.. code-block:: python

    MIDDLEWARE = [
        'django_guid.middleware.GuidMiddleware',
        ...
     ]


It is recommended that you add the middleware at the top, so that the remaining middleware loggers include the requests GUID.

2. Configuring Logging
======================

Add :code:`django_guid.log_filters.CorrelationId` as a filter in your ``LOGGING`` configuration:

.. code-block:: python

    LOGGING = {
        ...
        'filters': {
            'correlation_id': {
                '()': 'django_guid.log_filters.CorrelationId'
            }
        }
    }

Put that filter in your handler:

.. code-block:: python

    LOGGING = {
        ...
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'medium',
                'filters': ['correlation_id'],
            }
        }
    }

And make sure to add the new ``correlation_id`` filter to one or all of your formatters:

.. code-block:: python

    LOGGING = {
        ...
        'formatters': {
            'medium': {
                'format': '%(levelname)s %(asctime)s [%(correlation_id)s] %(name)s %(message)s'
            }
        }
    }


If these settings were confusing, please have a look in the demo project's
`settings.py <https://github.com/JonasKs/django-guid/blob/master/demoproj/settings.py>`_ file for a complete example.

3. Adding the Django GUID logger
================================

If you wish to see the Django GUID middleware outputs, you may configure a logger for the module.
Simply add django_guid to your loggers in the project, like in the example below:

.. code-block:: python

    LOGGING = {
        ...
        'loggers': {
            'django_guid': {
                'handlers': ['console', 'logstash'],
                'level': 'WARNING',
                'propagate': False,
            }
        }
    }



----------

This package was inspired by `django-log-request-id <https://github.com/dabapps/django-log-request-id>`_ with a complete rewritten
`django-echelon <https://github.com/seveas/django-echelon>`_ approach.
