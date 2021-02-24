Changelog
=========


`2.2.1`_ - 2020-02-16
---------------------
**Package bugfix**

* Fixes #56. Making `setup.py install`  possible.


`2.2.0`_ - 2020-11-04
---------------------
**Features**

* ``IGNORE_URLS`` setting which disables the middleware on a list of URLs.

**Other**

* Added docs for the new setting


`2.1.0`_ - 2020-11-03
---------------------
**Features**

* Integration module, which enables the users of ``django_guid`` to extend functionality.
* Added a integration for Sentry, tagging the Sentry issue with the GUID used for the request.

**Other**

* Added docs for integrations


`2.0.0`_ - 2020-03-02
---------------------
**This version contains backwards incompatible changes. Read the entire changelog before upgrading**


**Deprecated**

* ``SKIP_CLEANUP``: After a request is finished, the Correlation ID is cleaned up using the ``request_finished`` Django signal.


**Incompatible changes**

* ``django_guid`` must be in ``INSTALLED_APPS`` due to usage of signals.


**Improvements**

* Restructured README and docs.


`1.1.1`_ - 2020-02-12
---------------------

**Improvements**

* Fixed ``EXPOSE_HEADER`` documentation issue. New release has to be pushed to fix PyPi docs.


`1.1.0`_ - 2020-02-10
---------------------

**Features**

* Added a ``EXPOSE_HEADER`` setting, which will add the ``Access-Control-Expose-Headers`` with the ``RETURN_HEADER`` as value to the response. This is to allow the JavaScript Fetch API to access the header with the GUID



`1.0.1`_ - 2020-02-08
---------------------

**Bugfix**

* Fixed validation of incoming GUID

**Improvements**

* Changed the ``middleware.py`` logger name to ``django_guid``

* Added a WARNING-logger for when validation fails

* Improved README

**Other**

* Added ``CONTRIBUTORS.rst``



`1.0.0`_ - 2020-01-14
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



`0.3.1`_ - 2020-01-13
---------------------

**Improvements**

* Changed logging from f'strings' to %strings

* Pre-commit hooks added, including ``black`` and ``flake8``

* Added ``CONTRIBUTING.rst``

* Added github actions to push to ``PyPi`` with github tags



`0.3.0`_ - 2020-01-10
---------------------

**Features**

* Added a SKIP_CLEANUP setting

**Improvements**

* Improved all tests to be more verbose

* Improved the README with more information and a list of all the available settings


`0.2.3`_ - 2020-01-09
---------------------

**Improvements**

* Added tests written in `pytests`, 100% codecov

* Added Django2.2 and Django3 to github workflow as two steps

* Improved logging


`0.2.2`_ - 2019-12-21
---------------------

**Improvements**

* Removed the mandatory DJANGO_GUID settings in settings.py. Added an example project to demonstrate how to set the project up


`0.2.1`_ - 2019-12-21
---------------------

**Improvements**

* Workflow added, better docstrings, easier to read flow


`0.2.0`_ - 2019-12-21
---------------------

**Features**

* Header name and header GUID validation can be specified through Django settings

2019-12-20
------------------

* Initial release


.. _0.2.0: https://github.com/jonasks/django-guid/compare/0.1.2...0.2.0
.. _0.2.1: https://github.com/jonasks/django-guid/compare/0.2.0...0.2.1
.. _0.2.2: https://github.com/jonasks/django-guid/compare/0.2.1...0.2.2
.. _0.2.3: https://github.com/jonasks/django-guid/compare/0.2.2...0.2.3
.. _0.3.0: https://github.com/jonasks/django-guid/compare/0.2.3...0.3.0
.. _0.3.1: https://github.com/jonasks/django-guid/compare/0.3.0...0.3.1
.. _1.0.0: https://github.com/jonasks/django-guid/compare/0.3.0...1.0.0
.. _1.0.1: https://github.com/jonasks/django-guid/compare/1.0.0...1.0.1
.. _1.1.0: https://github.com/jonasks/django-guid/compare/1.0.1...1.1.0
.. _1.1.1: https://github.com/jonasks/django-guid/compare/1.1.0...1.1.1
.. _2.0.0: https://github.com/jonasks/django-guid/compare/1.1.1...2.0.0
.. _2.1.0: https://github.com/jonasks/django-guid/compare/2.0.0...2.1.0
.. _2.2.0: https://github.com/jonasks/django-guid/compare/2.1.0...2.2.0
.. _2.2.1: https://github.com/jonasks/django-guid/compare/2.2.0...2.2.1
