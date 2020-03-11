.. _integrations:

************
Integrations
************

Integrations can be used to add extra steps into the middleware.
To enable an integration, populate the ``INTEGRATIONS`` field in ``settings.py``.


Writing your own integration
============================

First, create a class that inherits the ``Integration`` base class and set the ``identifier`` variable:

.. code-block:: python

    from django_guid.integrations import Integration

    class CustomIntegration(Integration):

        identifier = 'CustomIntegration'  # Should be a string


There are four built in methods which are always called. You can chose to override these in your custom
integration.


validate(self)
--------------

The ``validate`` function will be run when Django starts, and should only handle validation logic,
such as checking if a third party package is installed.

Example:

.. code-block:: python

    class CustomIntegration(Integration):
        def validate(self):
            try:
                import third_party_sdk
            except ModuleNotFoundError:
                raise ImproperlyConfigured(
                    'Package third_party_sdk must be installed'
                )



setup(self)
-----------

The ``setup`` function hold logic to be run once the middleware is initialized. This will only happen once.

Example:

.. code-block:: python

    from third_party_sdk import start_service

    class CustomIntegration(Integration):
        def setup(self):
            start_service()



def run(self, guid, \*\*kwargs)
-------------------------------

Code to be executed for each time the middleware is run, before the view is called.
This function **must** accept both ``guid`` and ``**kwargs``. Like Django signals there may be added additional arguments
at a later point in time, so the function must be able to handle those new arguments.

Example:

.. code-block:: python

    from third_party_sdk import send_guid_to_system

    class CustomIntegration(Integration):
        def run(self, guid, **kwargs):
            send_guid_to_system(guid=guid)



def tear_down(self, \*\*kwargs):
--------------------------------

Code to be executed each time the middleware is run, after a view has been called.
This function **must** accept ``**kwargs``. Like Django signals there may be added additional arguments
at a later point in time, so the function must be able to handle those new arguments.

Example:

.. code-block:: python

    from third_party_sdk import clean_up_guid

    class CustomIntegration(Integration):
        def tear_down(self, **kwargs):
            clean_up_guid()


Shipped integrations
====================
Django GUID ships with the following integrations, and pull requests for more are welcome:

SentryIntegration
-----------------

The ``SentryIntegration`` sets the ``transaction_id`` of ``Sentry`` to match the GUID used in the middleware.

Implement by adding the integrations to your ``DJANGO_GUID`` settings:

.. code-block:: python

    from django_guid.integrations import SentryIntegration
    DJANGO_GUID = {
        GUID_HEADER_NAME = 'Correlation-ID',
        INTEGRATIONS = [SentryIntegration()],
    }
