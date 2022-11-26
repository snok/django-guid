# Celery integration

Example code for setting up correlation IDs and Celery IDs.

To demo, run

- `docker compose up -d`, or run redis locally on port 6378 (or change the example broker URL in settings.py)
- Run a celery worker with `celery -A src worker`
- Queue a task by running:
    ```
    python manage.py shell<<EOF
    from src.celery import debug_task
    debug_task.delay()
    EOF
    ```

You should see output that looks something like this:

```
INFO [23c3159e8a] [None-12f63b4fa2] src.celery - debug task 1
INFO [23c3159e8a] [12f63b4fa2-5447ee7603] src.celery - debug task 2
INFO [23c3159e8a] [12f63b4fa2-e51d63a22e] src.celery - debug task 2
INFO [23c3159e8a] [e51d63a22e-c6fdd30fab] src.celery - debug task 3
INFO [23c3159e8a] [e51d63a22e-c66b22b1a3] src.celery - debug task 4
INFO [23c3159e8a] [5447ee7603-cadfb62a6e] src.celery - debug task 3
INFO [23c3159e8a] [cadfb62a6e-51302bc9b6] src.celery - debug task 4
INFO [23c3159e8a] [5447ee7603-26a50bb2f8] src.celery - debug task 4
INFO [23c3159e8a] [cadfb62a6e-570b12a0f2] src.celery - debug task 4
INFO [23c3159e8a] [c6fdd30fab-fc1d7af723] src.celery - debug task 4
INFO [23c3159e8a] [c6fdd30fab-124ce2a10d] src.celery - debug task 4
```
