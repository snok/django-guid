Publish django-guid
===================

This site is intended for the contributors of ``django-guid``.

PyPi
----

Publishing ``django-guid`` can be done through tagging git commits. Any commits tagged with ``-rc`` will be published
to ``TestPyPi``, while any other tag will be released to ``PyPi``. It is important that the version we actually push
is defined in ``django_guid/__init__.py``, and the tag created to git is simply for git history.

.. code-block:: bash

    git tag 1.0.0-rc1  # Publishes to TestPyPi
    git tag 1.0.0      # Publishes to PyPi

Read the docs
-------------

Read the docs documentation can be built locally by entering the ``docs`` folder and writing ``make html``.
It requires that you have installed ``sphinx`` and the theme we're using, which is ``sphinx_rtd_theme``. Both can be
installed through ``pip``.
