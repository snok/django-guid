Installation
============

Requirements
------------

* Python 3.6 and above (May work on older versions too)
* Django 2.2 and above (Header setting used in the middleware was added in Django 2.2)

Package installation
--------------------

Install using pip:

    pip install django-guid


Then, in your project's :code:`settings.py` add these settings:

``-`` Add the middleware to the :code:`MIDDLEWARE` setting (if you want the correlation-ID to span your middleware-logs, put it on top):

.. code-block:: python

    MIDDLEWARE = [
        'django_guid.middleware.GuidMiddleware',
        ...
     ]


``-`` Add a filter to your ``LOGGING``:

.. code-block:: python

    LOGGING = {
        ...
        'filters': {
            'correlation_id': {
                '()': 'django_guid.log_filters.CorrelationId'
            }
        }
    }


::
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

+ Lastly make sure we add the new `correlation_id` filter to the formatters:

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

