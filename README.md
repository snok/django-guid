# Django GUID

[![package version](https://img.shields.io/pypi/v/django-guid.svg)](https://pypi.org/pypi/django-guid)
[![codecov](https://codecov.io/gh/snok/django-guid/branch/master/graph/badge.svg)](https://codecov.io/gh/snok/django-guid)
[![downloads](https://img.shields.io/badge/python-3.7+-blue.svg)](https://pypi.python.org/pypi/django-guid#downloads)
[![django versions](https://img.shields.io/pypi/djversions/django-guid?color=0C4B33&logo=django&logoColor=white&label=django)](https://pypi.python.org/pypi/django-guid)
[![asgi](https://img.shields.io/badge/ASGI-supported-brightgreen.svg)](https://img.shields.io/badge/ASGI-supported-brightgreen.svg)
[![wsgi](https://img.shields.io/badge/WSGI-supported-brightgreen.svg)](https://img.shields.io/badge/WSGI-supported-brightgreen.svg)


The middleware adds an ID to your logs that is unique to each incoming request. [Correlation IDs](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields?highlight=x-request-id#:~:text=Csrf%2DToken%3A%20i8XNjC4b8KVok4uw5RftR38Wgp2BFwql-,X%2DRequest%2DID,-%2C%5Bstackoverflow2%201)
(also knows as request IDs) make it easy to correlate logs from a single HTTP request, and makes debugging simple.

Django GUID also includes ways of extending correlation IDs to Celery workers and Sentry issues.

For the purposes of this package, a GUID (globally unique identifier) is equivalent
to a UUID (universally unique identifier).

## Examples

Let's assume we have three outgoing requests happening at the same time across our application instances:

```
INFO  project.views    Fetching resource
INFO  project.views    Fetching resource
INFO  project.views    Fetching resource
INFO  project.services Finished successfully
INFO  project.services Finished successfully
ERROR project.services Something went wrong!
```

Without a correlation-id we have no way of knowing which logs belong to which request.

Using a log filter, we can do a little better:

```
INFO  [773fa6885e03493498077a273d1b7f2d] project.views    Fetching resource
INFO  [0d1c3919e46e4cd2b2f4ac9a187a8ea1] project.views    Fetching resource
INFO  [99d44111e9174c5a9494275aa7f28858] project.views    Fetching resource
INFO  [99d44111e9174c5a9494275aa7f28858] project.services Finished successfully
INFO  [773fa6885e03493498077a273d1b7f2d] project.services Finished successfully
ERROR [0d1c3919e46e4cd2b2f4ac9a187a8ea1] project.services Something went wrong!
```

With the filter, we now know which logs belong to which request and can start debugging.

## Installation

```shell
pip install django-guid
```

## Settings

Package settings are added in your `settings.py`:

```python
DJANGO_GUID = {
    'GUID_HEADER_NAME': 'X-Request-ID',
    'VALIDATE_GUID': True,
    'RETURN_HEADER': True,
    'EXPOSE_HEADER': True,
    'INTEGRATIONS': [],
    'IGNORE_URLS': [],
    'UUID_LENGTH': 32,
}
```


**Optional Parameters**

* `GUID_HEADER_NAME`

  > The name of the GUID to look for in a header in an incoming request. Remember that it's case insensitive.

  Default: `Correlation-ID`

* `VALIDATE_GUID`
  > Whether the `GUID_HEADER_NAME` should be validated or not.
  If the GUID sent to through the header is not a valid GUID (`uuid.uuid4`).

  Default: `True`

* `RETURN_HEADER`
  > Whether to return the GUID (Correlation-ID) as a header in the response or not.
  It will have the same name as the `GUID_HEADER_NAME` setting.

  Default: `True`

* `EXPOSE_HEADER`
  > Whether to return `Access-Control-Expose-Headers` for the GUID header if
  `RETURN_HEADER` is `True`, has no effect if `RETURN_HEADER` is `False`.
  This is allows the JavaScript Fetch API to access the header when CORS is enabled.

  Default: `True`

* `INTEGRATIONS`
  > Whether to enable any custom or available integrations with `django_guid`.
  As an example, using `SentryIntegration()` as an integration would set Sentry's `transaction_id` to
  match the GUID used by the middleware.

  Default: `[]`

* `IGNORE_URLS`
  > URL endpoints where the middleware will be disabled. You can put your health check endpoints here.

  Default: `[]`

* `UUID_LENGTH`
  > Lets you optionally trim the length of the package generated UUIDs.

  Default: `32`

## Configuration


Once settings have set up, add the following to your projects' `settings.py`:

### 1. Installed apps

Add `django_guid` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django_guid',
]
```

### 2. Middleware

Add the `django_guid.middleware.guid_middleware` to your `MIDDLEWARE`:

```python
MIDDLEWARE = [
    'django_guid.middleware.guid_middleware',
    ...
 ]
```

It is recommended that you add the middleware at the top, so that the remaining middleware loggers include the requests GUID.

### 3. Logging configuration

Add `django_guid.log_filters.CorrelationId` as a filter in your `LOGGING` configuration:

```python
LOGGING = {
    ...
    'filters': {
        'correlation_id': {
            '()': 'django_guid.log_filters.CorrelationId'
        }
    }
}
```

Put that filter in your handler:

```python
LOGGING = {
    ...
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'medium',
            'filters': ['correlation_id'],
        }
    }
}
```

And make sure to add the new `correlation_id` filter to one or all of your formatters:

```python
LOGGING = {
    ...
    'formatters': {
        'medium': {
            'format': '%(levelname)s %(asctime)s [%(correlation_id)s] %(name)s %(message)s'
        }
    }
}
```

If these settings were confusing, you might find the repo examples helpful.

### 4. Django GUID logger (optional)

If you wish to see the Django GUID middleware outputs, you may configure a logger for the module.
Simply add django_guid to your loggers in the project, like in the example below:

```python
LOGGING = {
    ...
    'loggers': {
        'django_guid': {
            'handlers': ['console', 'logstash'],
            'level': 'WARNING',
            'propagate': False,
        }
    }
}
```

This could be useful for debugging problems with request ID propagation. If a received request header containing a request ID is misconfigured, we will not raise exceptions, but will generate warning logs.
