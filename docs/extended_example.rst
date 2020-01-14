.. _extended_example:

Extended example
================

Using tools like ``ab`` (`Apache Benchmark <https://httpd.apache.org/docs/2.4/programs/ab.html>`_) we can benchmark our application with concurrent requests, simulating
heavy load. This is an easy way to display the strength of ``django-guid``.

Experiment
----------

First, we run our application like we would in a production environment:

.. code-block:: bash

    gunicorn demoproj.wsgi:application --bind 127.0.0.1:8080 -k gthread -w 4

Then, we do 3 concurrent requests to one of our endpoints:

.. code-block:: bash

    ab -c 3 -n 3 http://127.0.0.1:8080/api


This results in these logs:

.. code-block:: bash

    django-guid git:(master) ✗ gunicorn demoproj.wsgi:application --bind 127.0.0.1:8080 -k gthread -w 4

    [2020-01-14 16:36:15 +0100] [8624] [INFO] Starting gunicorn 20.0.4
    [2020-01-14 16:36:15 +0100] [8624] [INFO] Listening at: http://127.0.0.1:8080 (8624)
    [2020-01-14 16:36:15 +0100] [8624] [INFO] Using worker: gthread
    [2020-01-14 16:36:15 +0100] [8627] [INFO] Booting worker with pid: 8627
    [2020-01-14 16:36:15 +0100] [8629] [INFO] Booting worker with pid: 8629
    [2020-01-14 16:36:15 +0100] [8630] [INFO] Booting worker with pid: 8630
    [2020-01-14 16:36:15 +0100] [8631] [INFO] Booting worker with pid: 8631

    # First request
    INFO 2020-01-14 15:40:48,953 [None] django_guid.middleware No Correlation-ID found in the header. Added Correlation-ID: 773fa6885e03493498077a273d1b7f2d
    INFO 2020-01-14 15:40:48,954 [773fa6885e03493498077a273d1b7f2d] demoproj.views This is a DRF view log, and should have a GUID.
    WARNING 2020-01-14 15:40:48,954 [773fa6885e03493498077a273d1b7f2d] demoproj.services.useless_file Some warning in a function
    DEBUG 2020-01-14 15:40:48,954 [773fa6885e03493498077a273d1b7f2d] django_guid.middleware Deleting 773fa6885e03493498077a273d1b7f2d from _guid

    # Second and third request arrives at the same time
    INFO 2020-01-14 15:40:48,955 [None] django_guid.middleware No Correlation-ID found in the header. Added Correlation-ID: 0d1c3919e46e4cd2b2f4ac9a187a8ea1
    INFO 2020-01-14 15:40:48,955 [None] django_guid.middleware No Correlation-ID found in the header. Added Correlation-ID: 99d44111e9174c5a9494275aa7f28858
    INFO 2020-01-14 15:40:48,955 [0d1c3919e46e4cd2b2f4ac9a187a8ea1] demoproj.views This is a DRF view log, and should have a GUID.
    INFO 2020-01-14 15:40:48,955 [99d44111e9174c5a9494275aa7f28858] demoproj.views This is a DRF view log, and should have a GUID.
    WARNING 2020-01-14 15:40:48,955 [0d1c3919e46e4cd2b2f4ac9a187a8ea1] demoproj.services.useless_file Some warning in a function
    WARNING 2020-01-14 15:40:48,955 [99d44111e9174c5a9494275aa7f28858] demoproj.services.useless_file Some warning in a function
    DEBUG 2020-01-14 15:40:48,955 [0d1c3919e46e4cd2b2f4ac9a187a8ea1] django_guid.middleware Deleting 0d1c3919e46e4cd2b2f4ac9a187a8ea1 from _guid
    DEBUG 2020-01-14 15:40:48,955 [99d44111e9174c5a9494275aa7f28858] django_guid.middleware Deleting 99d44111e9174c5a9494275aa7f28858 from _guid

If we have a close look, we can see that the first request is completely done before the second and third arrives.
How ever, the second and third request arrives at the exact same time, and since ``gunicorn`` is run with multiple workers,
they are also handled concurrently. The result is logs that get mixed together, making them impossible to differentiate.

Now, depending on how you view your logs you can easily track a single request down. In these docs, try using ``ctrl`` + ``f``
and search for ``99d44111e9174c5a9494275aa7f28858``

If you're logging to a file you could use ``grep``:


.. code-block:: bash

    ➜  ~ cat demoproj/logs.log | grep 99d44111e9174c5a9494275aa7f28858

    INFO 2020-01-14 15:40:48,955 [None] django_guid.middleware No Correlation-ID found in the header. Added Correlation-ID: 99d44111e9174c5a9494275aa7f28858
    INFO 2020-01-14 15:40:48,955 [99d44111e9174c5a9494275aa7f28858] demoproj.views This is a DRF view log, and should have a GUID.
    WARNING 2020-01-14 15:40:48,955 [99d44111e9174c5a9494275aa7f28858] demoproj.services.useless_file Some warning in a function
    DEBUG 2020-01-14 15:40:48,955 [99d44111e9174c5a9494275aa7f28858] django_guid.middleware Deleting 99d44111e9174c5a9494275aa7f28858 from _guid
