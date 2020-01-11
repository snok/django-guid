Installation
============

Requirements
------------

* Python 3.6 and above (May work on older versions too)
* Django 2.2 and above (Header setting used in the middleware was added in Django 2.2)

Package installation
--------------------

Python package::

    pip install django-auth-adfs


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
