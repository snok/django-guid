GUID injection for Django
=========================

.. image:: https://img.shields.io/pypi/v/django-guid.svg
    :target: https://pypi.python.org/pypi/django-guid
.. image:: https://img.shields.io/pypi/pyversions/django-guid.svg
    :target: https://pypi.python.org/pypi/django-guid#downloads
.. image:: https://img.shields.io/pypi/djversions/django-guid.svg
    :target: https://pypi.python.org/pypi/django-guid

Django GUID stores a GUID to an object, making it accessible by using the ID of the current thread.
The GUID is accessible from anywhere within the application throughout a request,
allowing us to inject it into the logs.

* Free software: BSD License
* Homepage: https://github.com/JonasKs/django-guid
* Documentation: https://django-guid.readthedocs.io


Contents
--------

.. toctree::
    :maxdepth: 3

    install
    settings
    troubleshooting
    changelog
