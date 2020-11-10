from contextvars import ContextVar

guid: ContextVar = ContextVar('guid', default=None)
