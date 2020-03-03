************
Installation
************

Install using pip:

.. code-block:: bash

    pip install django-guid



Configuration
=============

Once settings have set up, add the following to your projects' ``settings.py``:


1. Installed Apps
-----------------

Add :code:`django_guid` to your :code:`INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django_guid',
    ]



2. Middleware
-------------

Add the :code:`django_guid.middleware.GuidMiddleware` to your ``MIDDLEWARE``:

.. code-block:: python

    MIDDLEWARE = [
        'django_guid.middleware.GuidMiddleware',
        ...
     ]


It is recommended that you add the middleware at the top, so that the remaining middleware loggers include the requests GUID.

3. Logging Configuration
------------------------

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


If these settings were confusing, please have a look in the demo projects'
`settings.py <https://github.com/JonasKs/django-guid/blob/master/demoproj/settings.py>`_ file for a complete example.

4. Django GUID Logger (Optional)
--------------------------------

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

This is especially useful when implementing the package, if you plan to pass existing GUIDs to the middleware, as misconfigured GUIDs will not raise exceptions, but will generate warning logs.
