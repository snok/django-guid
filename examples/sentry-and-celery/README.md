# Sentry and Celery-integration

To enable the Sentry integration in a Celery context, set `sentry_integration=True`
when instantiating the `CeleryIntegration` class.

Beyond that, take a look at the `celery` example for how to set up the celery integration in more detail.

```python
from django_guid.integrations import SentryIntegration, CeleryIntegration

DJANGO_GUID = {
    'INTEGRATIONS': [
        SentryIntegration(),
        CeleryIntegration(sentry_integration=True)
    ]
}
```
