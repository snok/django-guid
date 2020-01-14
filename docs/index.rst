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


Example
-------

Using ``demoproj`` as an example, all the log messages **without** ``django-guid`` would look like this:

.. code-block:: bash

    INFO 2020-01-14 12:28:42,194 django_guid.middleware No Correlation-ID found in the header. Added Correlation-ID: 97c304252fd14b25b72d6aee31565843
    INFO 2020-01-14 12:28:42,353 demoproj.views This is a DRF view log, and should have a GUID.
    INFO 2020-01-14 12:28:42,354 demoproj.services.useless_file Some warning in a function

With ``django-guid`` every log message has a GUID (``97c304252fd14b25b72d6aee31565843``) attached to it,
through the entire stack:

.. code-block:: bash

    INFO 2020-01-14 12:28:42,194 [None] django_guid.middleware No Correlation-ID found in the header. Added Correlation-ID: 97c304252fd14b25b72d6aee31565843
    INFO 2020-01-14 12:28:42,353 [97c304252fd14b25b72d6aee31565843] demoproj.views This is a DRF view log, and should have a GUID.
    INFO 2020-01-14 12:28:42,354 [97c304252fd14b25b72d6aee31565843] demoproj.services.useless_file Some warning in a function


Why
---

``django-guid`` makes it extremely easy to track exactly what happened in any request. If you see one error
in your log, you can use the attached GUID to search for any connected log message to that single request.
The GUID can also be returned as a header and displayed to the end user of your application, allowing them
to report an issue with a connected ID. ``django-guid`` makes troubleshooting easy.


Contents
--------

.. toctree::
    :maxdepth: 3

    install
    settings
    api
    troubleshooting
    contributing
    publish
    changelog
