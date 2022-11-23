# Sentry integration

Shows how to add the Sentry integration. There's not an easy
way to demonstrate how this works, since you'd be dependent
on Sentry to demonstrate. As a consequence, this just includes
the configuration itself:

```python
from django_guid.integrations import SentryIntegration

DJANGO_GUID = {
    'INTEGRATIONS': [
        SentryIntegration()
    ]
}
```
