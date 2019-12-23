GUID injection for Django
=========================

.. image:: https://img.shields.io/pypi/v/django-guid.svg
    :target: https://pypi.python.org/pypi/django-guid
.. image:: https://img.shields.io/pypi/pyversions/django-guid.svg
    :target: https://pypi.python.org/pypi/django-guid#downloads
.. image:: https://img.shields.io/pypi/djversions/django-guid.svg
    :target: https://pypi.python.org/pypi/django-guid

Django GUID attaches a GUID to the local thread of a request.   
The GUID is accessible from anywhere within the application throughout a request, making it possible to 
inject the GUID into the logs.

* Free software: BSD License
* Homepage: https://github.com/JonasKs/django-guid
* Documentation: Incoming

Installation
------------

Python package::

    pip install django-guid

In your project's ``settings.py`` add these settings:

Add the middleware to the middleware (To ensure the GUID to be injected in all logs, put it on top)

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

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'medium',
            'filters': ['correlation_id'],
        }
    }

and lastly make sure we add it to the format:

.. code-block:: python

    'medium': {
        'format': '%(levelname)s %(asctime)s [%(correlation_id)s] %(name)s %(message)s'
    }

Inspired by `django-log-request-id <https://github.com/dabapps/django-log-request-id>`_ with a
`django-crequest <https://github.com/Alir3z4/django-crequest>`_ approach.
