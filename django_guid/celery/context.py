from contextvars import ContextVar

celery: ContextVar = ContextVar('celery', default=None)
