Publish django-guid
===================

This site is intended for the contributors of ``django-guid``.

Publishing to test-PyPi
-----------------------

Before publishing a new version of the package, it is advisable that you publish a test-package. Among other things, this will flag any possible issues the current interation of the package might have.

Please note, to publish a test-package, you need to have a test-pypi API token.

Using the API token, you can publish a test-package by running:

.. code::

    poetry config repositories.test https://test.pypi.org/legacy/
    poetry config pypi-token.test <api-token>
    poetry publish --build --no-interaction --repository test

Publishing to PyPi
------------------

Publishing ``django-guid`` can be done by creating a github release in the ``django-guid`` repository. Before publishing a release, make sure that the version is consistent in ``django_guid/__init__.py``, ``pyproject.toml`` and in the title of the actual publication. The title of the release should simply be the version number and the release body should contain the changelog for the patch.

Read the docs
-------------

Read the docs documentation can be built locally by entering the ``docs`` folder and writing ``make html``.
It requires that you have installed ``sphinx`` and the theme we're using, which is ``sphinx_rtd_theme``. Both can be
installed through ``pip``.
