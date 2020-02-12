Django GUID
===========

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


Django GUID stores a GUID to an object, making it accessible by using the ID of the current thread.
The GUID is accessible from anywhere within the application throughout a request,
allowing us to inject it into the logs.

* Free software: BSD License
* Homepage: https://github.com/JonasKs/django-guid
* Documentation: https://django-guid.readthedocs.io


Example
-------

Using ``demoproj`` as an example, all the log messages **without** ``django-guid`` would look like this:

.. code-block:: bash

    INFO 2020-01-14 12:28:42,194 django_guid.middleware No Correlation-ID found in the header. Added Correlation-ID: 97c304252fd14b25b72d6aee31565843
    INFO 2020-01-14 12:28:42,353 demoproj.views This is a DRF view log, and should have a GUID.
    INFO 2020-01-14 12:28:42,354 demoproj.services.useless_file Some warning in a function


With ``django-guid`` every log message has a GUID attached to it(``97c304252fd14b25b72d6aee31565843``),
through the entire stack:

.. code-block:: bash

    INFO 2020-01-14 12:28:42,194 [None] django_guid.middleware No Correlation-ID found in the header. Added Correlation-ID: 97c304252fd14b25b72d6aee31565843
    INFO 2020-01-14 12:28:42,353 [97c304252fd14b25b72d6aee31565843] demoproj.views This is a DRF view log, and should have a GUID.
    INFO 2020-01-14 12:28:42,354 [97c304252fd14b25b72d6aee31565843] demoproj.services.useless_file Some warning in a function

For multiple requests at the same time over multiple threads, see the `extended example docs <https://django-guid.readthedocs.io/en/latest/extended_example.html>`_.


Why
---

``django-guid`` makes it extremely easy to track exactly what happened in any request. If you see an error
in your log, you can use the attached GUID to search for any connected log message to that single request.
The GUID can also be returned as a header and displayed to the end user of your application, allowing them
to report an issue with a connected ID. ``django-guid`` makes troubleshooting easy.


Settings
--------

* :code:`SKIP_CLEANUP`
        After the request is done, the GUID is deleted to avoid memory leaks. Memory leaks can happen in the
        case of many threads, or especially when using Gunicorn :code:`max_requests` or similar settings,
        where the number of thread IDs can potentially scale for ever.
        Having clean up enabled ensures we can not have memory leaks, but comes at the cost that anything that happens
        after this middleware will not have the GUID attached, such as :code:`django.request` or :code:`django.server`
        logs. If you do not want clean up of GUIDs and know what you're doing, you can enable :code:`SKIP_CLEANUP`.

    Default: False

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


Installation
------------

Install using pip:

    pip install django-guid


Then, in your project's :code:`settings.py` add these settings:

Add the middleware to the :code:`MIDDLEWARE` setting (if you want the correlation-ID to span your middleware-logs, put it on top):

.. code-block:: python

    MIDDLEWARE = [
        'django_guid.middleware.GuidMiddleware',
        ...
     ]


Add a filter to your ``LOGGING``:

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

Lastly make sure we add the new ``correlation_id`` filter to the formatters:

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



If you wish to aggregate the django-guid logs to your console or other handlers, add django_guid to your loggers in the project. Example:

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

Inspired by `django-log-request-id <https://github.com/dabapps/django-log-request-id>`_ with a complete rewritten
`django-echelon <https://github.com/seveas/django-echelon>`_ approach.
