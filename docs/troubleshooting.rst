Troubleshooting
===============

Turn on Django debug logging
----------------------------

Set the logger to log DEBUG logs from django-guid:

.. code-block:: python

    LOGGING = {
        'loggers': {
            'django-guid': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }



Run Django with warnings enabled
--------------------------------
Start ``manage.py runserver``  with the ``-Wd`` parameter to enable warnings that normally are suppressed.

.. code-block:: bash

    python -Wd manage.py runserver


Use the demo project as a reference
-----------------------------------
There is a simple demo project available in the ``demoproj`` folder, have a look at that to see best practices.


Read the official logging docs
------------------------------
Read the `official docs <https://docs.djangoproject.com/en/dev/topics/logging/>`_ about logging.


Ask for help
------------
Still no luck? Create an `issue on GitHub <https://github.com/JonasKs/django-guid/issues/new/choose>`_ and ask for help.
