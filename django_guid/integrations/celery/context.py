from contextvars import ContextVar

celery_parent: ContextVar = ContextVar('celery_parent', default=None)
celery_current: ContextVar = ContextVar('celery_current', default=None)
