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


Installation
------------

Python package::

    pip install django-guid

In your project's :code:`settings.py` add these settings:

(If these settings are confusing, please have a look in the demo project
`settings.py <https://github.com/JonasKs/django-guid/blob/master/demoproj/settings.py>`_ file for a complete setup.)


Add the middleware to the :code:`MIDDLEWARE` setting (To ensure the GUID to be injected in all logs, put it on top):

.. code-block:: python

    MIDDLEWARE = [
        'django_guid.middleware.GuidMiddleware',
        ...
     ]


Add a filter to your ``LOGGING``:

.. code-block:: python

    LOGGING = {
        'filters': {
            'correlation_id': {
                '()': 'django_guid.log_filters.CorrelationId'
            }
        }
    }


and put that filter in your handler:

.. code-block:: python

    LOGGING = {
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'medium',
                'filters': ['correlation_id'],
            }
        }
    }

and lastly make sure we add the new `correlation_id` filter to the formatters:

.. code-block:: python

    LOGGING = {
        'formatters': {
            'medium': {
                'format': '%(levelname)s %(asctime)s [%(correlation_id)s] %(name)s %(message)s'
            }
        }
    }


Inspired by `django-log-request-id <https://github.com/dabapps/django-log-request-id>`_ with a
`django-crequest <https://github.com/Alir3z4/django-crequest>`_ approach.
