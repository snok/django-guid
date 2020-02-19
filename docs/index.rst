###########
Django GUID
###########

.. image:: https://img.shields.io/pypi/v/django-guid.svg
    :target: https://pypi.python.org/pypi/django-guid
.. image:: https://img.shields.io/pypi/pyversions/django-guid.svg
    :target: https://pypi.python.org/pypi/django-guid#downloads
.. image:: https://img.shields.io/pypi/djversions/django-guid.svg
    :target: https://pypi.python.org/pypi/django-guid
.. image:: https://readthedocs.org/projects/django-guid/badge/?version=latest
    :target: https://django-guid.readthedocs.io/en/latest/?badge=latest
.. image:: https://codecov.io/gh/jonasks/django-guid/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jonasks/django-guid
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://django-guid.readthedocs.io/en/latest/?badge=latest
.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit


Django GUID attaches a unique correlation ID to all your log outputs for every requests you handle. In other words, every error, and really every log now has an ID connecting it to all other relevant logs, making
debugging simple.

The package stores a GUID to an object, making it accessible by using the ID of the current thread. This makes integrations possible, as the ID can be returned as a header (built in setting) or forwarded manually to other systems (built in API), making it possible to extend the reach of correlation IDs to whole systems.

**Resources**:

* Free software: BSD License
* Documentation: https://django-guid.readthedocs.io
* Homepage: https://github.com/JonasKs/django-guid

**Examples**

Log output with a GUID:

.. code-block:: none

    INFO ... [773fa6885e03493498077a273d1b7f2d] project.views This is a DRF view log, and should have a GUID.
    WARNING ... [773fa6885e03493498077a273d1b7f2d] project.services.file Some warning in a function
    INFO ... [0d1c3919e46e4cd2b2f4ac9a187a8ea1] project.views This is a DRF view log, and should have a GUID.
    INFO ... [99d44111e9174c5a9494275aa7f28858] project.views This is a DRF view log, and should have a GUID.
    WARNING ... [0d1c3919e46e4cd2b2f4ac9a187a8ea1] project.services.file Some warning in a function
    WARNING ... [99d44111e9174c5a9494275aa7f28858] project.services.file Some warning in a function


Log output without a GUID:

.. code-block:: none

    INFO ... project.views This is a DRF view log, and should have a GUID.
    WARNING ... project.services.file Some warning in a function
    INFO ... project.views This is a DRF view log, and should have a GUID.
    INFO ... project.views This is a DRF view log, and should have a GUID.
    WARNING ... project.services.file Some warning in a function
    WARNING ... project.services.file Some warning in a function

Contents
--------

.. toctree::
    :maxdepth: 3

    install
    settings
    api
    extended_example
    troubleshooting
    contributing
    publish
    changelog
