# Django GUID Injection
Django GUID injection spawns a local thread for each request and stores a GUID in the thread.  
The thread is accessible from anywhere within the application throughout a request, making it possible to 
inject the request into the logs.

# Installation
Will come on PyPi soon™

# Usage:
Add a filter to your `LOGGING`:
```python
'filters': {
    'correlation_id': {
        '()': 'django_guid_injection.log_filters.CorrelationId'
    }
}
```
and put that filter in your handler:
```python
'handlers': {
    'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'medium',
        'filters': ['correlation_id'],
    }
}
```
and lastly make sure we add it to the format:
```python
'medium': {
    'format': '%(levelname)s %(asctime)s [%(correlation_id)s] %(name)s %(message)s'
},
```


Inspired by [django-log-request-id](https://github.com/dabapps/django-log-request-id) with a 
[django-crequest](https://github.com/Alir3z4/django-crequest) approach.