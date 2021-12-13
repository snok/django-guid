Changelog
=========

`3.2.1`_ - 13.12.2021
---------------------
Changes can be seen here_ going forward.

`3.2.0`_ - 04.12.2020
---------------------

**Features**

* Added a new setting, ``sentry_integration`` to the Celery integration, which sets ``transaction_id`` for Celery workers.

`3.1.0`_ - 18.11.2020
---------------------

**Features**

* Added a new setting, ``UUID_LENGTH``, which lets you crop the UUIDs generated for log filters.
* Added a new integration for tracing with Celery_.

`3.0.1`_ - 12.11.2020
---------------------

**Bugfix**

* Importing an integration before a ``SECRET_KEY`` was set would cause a circular import.


`3.0.0`_ - 28.10.2020 - Full Django3.1+(ASGI/async) support!
------------------------------------------------------------
Brings full async/ASGI (as well as the old WSGI) support to Django GUID using ContextVars instead of thread locals.

**Breaking changes**

This version requires ``Django>=3.1.1``. For previous versions of Django,
please use ``django-guid<3.0.0`` (Such as ``django-guid==2.2.0``).

If you've already implemented ``django-guid`` in your project and are currently upgrading to ``Django>=3.1.1``, please
see the `upgrading docs`_.


`2.2.0`_ - 04.11.2020
---------------------
**Features**

* ``IGNORE_URLS`` setting which disables the middleware on a list of URLs.

**Other**

* Added docs for the new setting


`2.1.0`_ - 03.11.2020
---------------------
**Features**

* Integration module, which enables the users of ``django_guid`` to extend functionality.
* Added a integration for Sentry, tagging the Sentry issue with the GUID used for the request.

**Other**

* Added docs for integrations


`2.0.0`_ - 02.03.2020
---------------------
**This version contains backwards incompatible changes. Read the entire changelog before upgrading**


**Deprecated**

* ``SKIP_CLEANUP``: After a request is finished, the Correlation ID is cleaned up using the ``request_finished`` Django signal.


**Incompatible changes**

* ``django_guid`` must be in ``INSTALLED_APPS`` due to usage of signals.


**Improvements**

* Restructured README and docs.


`1.1.1`_ - 12.02.2020
---------------------

**Improvements**

* Fixed ``EXPOSE_HEADER`` documentation issue. New release has to be pushed to fix PyPi docs.


`1.1.0`_ - 10.02.2020
---------------------

**Features**

* Added a ``EXPOSE_HEADER`` setting, which will add the ``Access-Control-Expose-Headers`` with the ``RETURN_HEADER`` as value to the response. This is to allow the JavaScript Fetch API to access the header with the GUID



`1.0.1`_ - 08.02.2020
---------------------

**Bugfix**

* Fixed validation of incoming GUID

**Improvements**

* Changed the ``middleware.py`` logger name to ``django_guid``

* Added a WARNING-logger for when validation fails

* Improved README

**Other**

* Added ``CONTRIBUTORS.rst``



`1.0.0`_ - 14.01.2020
---------------------

**Features**

* Added a ``RETURN_HEADER`` setting, which will return the GUID as a header with the same name


**Improvements**

* Added a Django Rest Framework test and added DRF to the ``demoproj``

* Improved tests to also check for headers in the response

* Added tests for the new setting

* Added examples to ``README.rst`` and docs, to show how the log messages get formatted

* Added an API page to the docs

* Fixed the ``readthedocs`` menu bug



`0.3.1`_ - 13.01.2020
---------------------

**Improvements**

* Changed logging from f'strings' to %strings

* Pre-commit hooks added, including ``black`` and ``flake8``

* Added ``CONTRIBUTING.rst``

* Added github actions to push to ``PyPi`` with github tags



`0.3.0`_ - 10.01.2020
---------------------

**Features**

* Added a SKIP_CLEANUP setting

**Improvements**

* Improved all tests to be more verbose

* Improved the README with more information and a list of all the available settings


`0.2.3`_ - 09.01.2020
---------------------

**Improvements**

* Added tests written in `pytests`, 100% codecov

* Added Django2.2 and Django3 to github workflow as two steps

* Improved logging


`0.2.2`_ - 21.12.2019
---------------------

**Improvements**

* Removed the mandatory DJANGO_GUID settings in settings.py. Added an example project to demonstrate how to set the project up


`0.2.1`_ - 21.12.2019
---------------------

**Improvements**

* Workflow added, better docstrings, easier to read flow


`0.2.0`_ - 21.12.2019
---------------------

**Features**

* Header name and header GUID validation can be specified through Django settings

20.10.2019
----------

* Initial release


.. _0.2.0: https://github.com/snok/django-guid/compare/0.1.2...0.2.0
.. _0.2.1: https://github.com/snok/django-guid/compare/0.2.0...0.2.1
.. _0.2.2: https://github.com/snok/django-guid/compare/0.2.1...0.2.2
.. _0.2.3: https://github.com/snok/django-guid/compare/0.2.2...0.2.3
.. _0.3.0: https://github.com/snok/django-guid/compare/0.2.3...0.3.0
.. _0.3.1: https://github.com/snok/django-guid/compare/0.3.0...0.3.1
.. _1.0.0: https://github.com/snok/django-guid/compare/0.3.0...1.0.0
.. _1.0.1: https://github.com/snok/django-guid/compare/1.0.0...1.0.1
.. _1.1.0: https://github.com/snok/django-guid/compare/1.0.1...1.1.0
.. _1.1.1: https://github.com/snok/django-guid/compare/1.1.0...1.1.1
.. _2.0.0: https://github.com/snok/django-guid/compare/1.1.1...2.0.0
.. _2.1.0: https://github.com/snok/django-guid/compare/2.0.0...2.1.0
.. _2.2.0: https://github.com/snok/django-guid/compare/2.1.0...2.2.0
.. _3.0.0: https://github.com/snok/django-guid/compare/2.2.0...3.0.0
.. _upgrading docs: https://django-guid.readthedocs.io/en/latest/upgrading.html
.. _3.0.1: https://github.com/snok/django-guid/compare/3.0.0...3.0.1
.. _3.1.0: https://github.com/snok/django-guid/compare/3.0.1...3.1.0
.. _3.2.0: https://github.com/snok/django-guid/compare/3.1.0...3.2.0
.. _3.2.1: https://github.com/snok/django-guid/compare/3.2.0...3.2.1

.. _Celery: https://docs.celeryproject.org/en/stable/
.. _here: https://github.com/snok/django-guid/releases
