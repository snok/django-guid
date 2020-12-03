.. _integrations:

************
Integrations
************

Integrations are optional add-ins used to extend the functionality of the Django GUID middleware.

To enable an integration, simply add an integration instance to the ``INTEGRATIONS`` field in ``settings.py``,
and the relevant integration logic will be executed in the middleware:

.. code-block:: python

    from django_guid.integrations import SentryIntegration

    DJANGO_GUID = {
        ...
        'INTEGRATIONS': [SentryIntegration()],
    }


Integrations are a new addition to Django GUID, and we plan to expand selection in the future. If you are looking for specific functionality that is not yet available, consider creating an issue, making a pull request, or writing your own private integration. Custom integrations classes are simple to write and can be implemented just like package integrations.

Available integrations
======================

Sentry
------

Integrating with Sentry, lets you tag Sentry-issues with a ``transaction_id``. This lets you easily connect an event in Sentry to your logs.

.. image:: img/sentry.png
  :width: 1600
  :alt: Alternative text

Rather than changing how Sentry works, this is just an additional piece of metadata that you can use to link sources of information
about an exception. If you know the GUID of an exception, you can find the relevant Sentry issue by searching for the tag:

.. image:: img/sentry_search.png
  :width: 1600
  :alt: Alternative text

To add the integration, simply import ``SentryIntegration`` from the integrations folder and add it to your settings:

.. code-block:: python

    from django_guid.integrations import SentryIntegration

    DJANGO_GUID = {
        ...
        'INTEGRATIONS': [SentryIntegration()],
    }

Celery
------

The Celery integration enables tracing for Celery workers. There's three possible scenarios:

1. A task is published from a request within Django
2. A task is published from another task
3. A task is published from Celery Beat

For scenario 1 and 2 the existing correlation IDs is transferred, and for scenario
3 a unique ID is generated.

To enable this behavior, simply add it to your list of integrations:

.. code-block:: python

    from django_guid.integrations import SentryIntegration

    DJANGO_GUID = {
        ...
        'INTEGRATIONS': [
            CeleryIntegration(
                use_django_logging=True,
                log_parent=True,
            )
        ],
    }

Integration settings
^^^^^^^^^^^^^^^^^^^^

These are the settings you can pass when instantiating the ``CeleryIntegration``:

* **use_django_logging**: Tells celery to use the Django logging configuration (formatter).
* **log_parent**: Enables the ``CeleryTracing`` log filter described below.
* **uuid_length**: Lets you optionally trim the length of the integration generated UUIDs.
* **sentry_integration**: If you use Sentry, enabling this setting will make sure ``transaction_id`` is set (like in the SentryIntegration) for Celery workers.

Celery integration log filter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Out of the box, the CeleryIntegration will make sure a correlation ID is present for any Celery task;
but how do you make sense of duplicate logs in subprocesses? Given these example tasks, what happens if we a worker
picks up ``debug_task`` as scheduled by Celery beat?

.. code-block:: python

    @app.task()
    def debug_task() -> None:
        logger.info('Debug task 1')
        second_debug_task.delay()
        second_debug_task.delay()


    @app.task()
    def second_debug_task() -> None:
        logger.info('Debug task 2')
        third_debug_task.delay()
        fourth_debug_task.delay()


    @app.task()
    def third_debug_task() -> None:
        logger.info('Debug task 3')
        fourth_debug_task.delay()
        fourth_debug_task.delay()


    @app.task()
    def fourth_debug_task() -> None:
        logger.info('Debug task 4')


It will be close to impossible to make sense of the logs generated,
simply because the correlation ID tells you nothing about how subprocesses are linked. For this,
the integration provides an additional log filter, ``CeleryTracing`` which logs the
ID of the current process and the ID of the parent process. Using the log filter, the log output of the example tasks becomes:

.. code-block:: bbcode

       correlation-id               current-id
              |        parent-id        |
              |            |            |
    INFO [3b162382e1] [   None   ] [93ddf3639c] demoproj.celery - Debug task 1
    INFO [3b162382e1] [93ddf3639c] [24046ab022] demoproj.celery - Debug task 2
    INFO [3b162382e1] [93ddf3639c] [cb5595a417] demoproj.celery - Debug task 2
    INFO [3b162382e1] [24046ab022] [08f5428a66] demoproj.celery - Debug task 3
    INFO [3b162382e1] [24046ab022] [32f40041c6] demoproj.celery - Debug task 4
    INFO [3b162382e1] [cb5595a417] [1c75a4ed2c] demoproj.celery - Debug task 3
    INFO [3b162382e1] [08f5428a66] [578ad2d141] demoproj.celery - Debug task 4
    INFO [3b162382e1] [cb5595a417] [21b2ef77ae] demoproj.celery - Debug task 4
    INFO [3b162382e1] [08f5428a66] [8cad7fc4d7] demoproj.celery - Debug task 4
    INFO [3b162382e1] [1c75a4ed2c] [72a43319f0] demoproj.celery - Debug task 4
    INFO [3b162382e1] [1c75a4ed2c] [ec3cf4113e] demoproj.celery - Debug task 4

At the very least, this should provide a mechanism for linking parent/children processes
in a meaningful way.

To set up the filter, add :code:`django_guid.integrations.celery.log_filters.CeleryTracing` as a filter in your ``LOGGING`` configuration:

.. code-block:: python

    LOGGING = {
        ...
        'filters': {
            'celery_tracing': {
                '()': 'django_guid.integrations.celery.log_filters.CeleryTracing'
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
                'filters': ['correlation_id', 'celery_tracing'],
            }
        }
    }

And then you can **optionally** add ``celery_parent_id`` and/or ``celery_current_id`` to you formatter:

.. code-block:: python

    LOGGING = {
        ...
        'formatters': {
            'medium': {
                'format': '%(levelname)s [%(correlation_id)s] [%(celery_parent_id)s-%(celery_current_id)s] %(name)s - %(message)s'
            }
        }
    }

However, if you use a log management tool which lets you interact with ``log.extra`` value, leaving the filters
out of the formatter might be preferable.

If these settings were confusing, please have a look in the demo projects'
`settings.py <https://github.com/snok/django-guid/blob/master/demoproj/settings.py>`_ file for a complete example.


Writing your own integration
============================

Creating your own custom integration requires you to inherit the ``Integration`` base class (which is found `here <https://github.com/snok/django-guid/tree/master/django_guid/integrations/base>`_).

The class is quite simple and only contains four methods and a class attribute:

.. code-block:: python

    class Integration(object):
        """
        Integration base class.
        """

        identifier = None  # The name of your integration

        def __init__(self) -> None:
            if self.identifier is None:
                raise ImproperlyConfigured('`identifier` cannot be None')

        def setup(self) -> None:
            """
            Holds validation and setup logic to be run when Django starts.
            """
            pass

        def run(self, guid: str, **kwargs) -> None:
            """
            Code here is executed in the middleware, before the view is called.
            """
            raise ImproperlyConfigured(f'The integration `{self.identifier}` is missing a `run` method')

        def cleanup(self, **kwargs) -> None:
            """
            Code here is executed in the middleware, after the view is called.
            """
            pass

To extend this into a fully functioning integration, all you need to do is

1. Create a new class that inherits the base class
2. Set the identifier to a string, naming your integration
3. Add the logic you wish to be executed to the ``run`` method
4. Add logic to each of the remaining methods as required

A fully functioning integration can be as simple as this:

.. code-block:: python

    from django_guid.integrations import Integration

    class CustomIntegration(Integration):

        identifier = 'CustomIntegration'  # Should be a string

        def run(self, guid, **kwargs):
            print('This is a functioning Django GUID integration')


There are four built in methods which are always called. You can chose to override these in your custom
integration.

Method descriptions
--------------------

Setup
^^^^^
The ``setup`` method is run when Django starts, and is a good place to keep your integration-specific validation logic,
like, e.g., making sure all dependencies are installed:

.. code-block:: python

    from third_party_sdk import start_service

    class CustomIntegration(Integration):

        identifier = 'CustomIntegration'

        def setup(self):
            try:
                import third_party_sdk
            except ModuleNotFoundError:
                raise ImproperlyConfigured(
                    'Package third_party_sdk must be installed'
                )


Run
^^^

The ``run`` method is required, and is designed to hold code that should be executed each time the middleware is run
(for each request made to the server), before the view is called.

This function **must** accept both ``guid`` and ``**kwargs``. Additional arguments are likely be added
in the future, and so the function must be able to handle those new arguments.

.. code-block:: python

    from third_party_sdk import send_guid_to_system

    class CustomIntegration(Integration):

        identifier = 'CustomIntegration'

        def setup(self):
            ...

        def run(self, guid, **kwargs):
            send_guid_to_system(guid=guid)



Cleanup
^^^^^^^

The ``cleanup`` method is the final method called in the middleware, each time the middleware, each time the middleware is run,
after a view has been called.

This function **must** accept ``**kwargs``. Additional arguments are likely be added
in the future, and so the function must be able to handle those new arguments.

.. code-block:: python

    from third_party_sdk import clean_up_guid

    class CustomIntegration(Integration):

        identifier = 'CustomIntegration'

        def setup(self):
            ...

        def run(self, guid, **kwargs):
            ...

        def cleanup(self, **kwargs):
            clean_up_guid()
