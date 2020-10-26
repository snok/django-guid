.. raw:: html

    <p align="center">
        <h1 align="center">Django GUID</h1>
    </p>
    <p align="center">
      <em>Now with ASGI support!</em>
    </p>

.. raw:: html

    <p align="center">
      <a href="https://pypi.org/pypi/django-guid">
          <img src="https://img.shields.io/pypi/v/django-guid.svg" alt="Package version">
      </a>
      <a href="https://pypi.python.org/pypi/django-guid#downloads">
          <img src="https://img.shields.io/badge/python-3.6+-blue.svg" alt="Downloads">
      </a>
      <a href="https://pypi.python.org/pypi/django-guid">
          <img src="https://img.shields.io/badge/django-2.2%20|%203.0%20|%203.1%20-blue.svg" alt="Django versions">
      </a>
      </a>
      <a href="https://img.shields.io/badge/ASGI-supported-brightgreen.svg">
          <img src="https://img.shields.io/badge/ASGI-supported-brightgreen.svg" alt="ASGI">
      </a>
      <a href="https://img.shields.io/badge/WSGI-supported-brightgreen.svg">
          <img src="https://img.shields.io/badge/WSGI-supported-brightgreen.svg" alt="WSGI">
      </a>
    </p>
    <p align="center">
      <a href="https://django-guid.readthedocs.io/en/latest/?badge=latest">
          <img src="https://readthedocs.org/projects/django-guid/badge/?version=latest" alt="Docs">
      </a>

      <a href="https://codecov.io/gh/snok/django-guid">
          <img src="https://codecov.io/gh/snok/django-guid/branch/master/graph/badge.svg" alt="Codecov">
      </a>

      <a href="https://github.com/psf/black">
          <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">
      </a>
      <a href="https://github.com/pre-commit/pre-commit">
          <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="Pre-commit">
      </a>
    </p>


--------------


Django GUID attaches a unique correlation ID/request ID to all your log outputs for every request.
In other words, all logs connected to a request now has a unique ID attached to it, making debugging simple.

To determine which Django-GUID version you should use, please see the table below.

+---------------------+--------------------------+
|   Django version    |   Django-GUID version    |
+=====================+==========================+
| 3.1.1 or above      |  3.x.x - ASGI and WSGI   |
+---------------------+--------------------------+
| 3.1.0               |  2.x.x - Only WSGI       |
+---------------------+--------------------------+
| 3.0.0               |  2.x.x - Only WSGI       |
+---------------------+--------------------------+
| 2.2.x               |  2.x.x - Only WSGI       |
+---------------------+--------------------------+

Django GUID >= 3.0.0 uses ``contextvars`` to store and access the GUID. Previous versions stored the GUID to an object,
making it accessible by using the ID of the current thread.

--------------

**Resources**:

* Free software: BSD License
* Documentation: https://django-guid.readthedocs.io
* Homepage: https://github.com/JonasKs/django-guid

--------------


**Examples**

Log output with a GUID:

.. code-block:: bbcode

    INFO ... [773fa6885e03493498077a273d1b7f2d] project.views This is a DRF view log, and should have a GUID.
    WARNING ... [773fa6885e03493498077a273d1b7f2d] project.services.file Some warning in a function
    INFO ... [0d1c3919e46e4cd2b2f4ac9a187a8ea1] project.views This is a DRF view log, and should have a GUID.
    INFO ... [99d44111e9174c5a9494275aa7f28858] project.views This is a DRF view log, and should have a GUID.
    WARNING ... [0d1c3919e46e4cd2b2f4ac9a187a8ea1] project.services.file Some warning in a function
    WARNING ... [99d44111e9174c5a9494275aa7f28858] project.services.file Some warning in a function


Log output without a GUID:

.. code-block:: text

    INFO ... project.views This is a DRF view log, and should have a GUID.
    WARNING ... project.services.file Some warning in a function
    INFO ... project.views This is a DRF view log, and should have a GUID.
    INFO ... project.views This is a DRF view log, and should have a GUID.
    WARNING ... project.services.file Some warning in a function
    WARNING ... project.services.file Some warning in a function


--------------


Contents
--------

.. toctree::
    :maxdepth: 3

    install
    settings
    api
    integrations
    extended_example
    troubleshooting
    contributing
    publish
    changelog
