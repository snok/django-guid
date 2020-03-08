from django.core.exceptions import ImproperlyConfigured


class Integration(object):
    """
    Integration base class.
    """

    identifier = None  # Name the identifier

    def __init__(self):
        """
        This is run when the integration is initialized in the clients settings.py.

        Put all validation logic here.
        """
        if self.identifier is None:
            raise ImproperlyConfigured('`identifier` cannot be None')

    def run(self, middleware_context) -> None:
        """
        Code here is executed in the middleware.
        """
        raise ImproperlyConfigured(f'The integration `{self.identifier}` is missing a `run` method')
