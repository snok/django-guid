from django.core.exceptions import ImproperlyConfigured


class Integration(object):
    """
    Integration base class.
    """

    identifier = None  # Name the identifier

    def __init__(self) -> None:
        if self.identifier is None:
            raise ImproperlyConfigured('`identifier` cannot be None')

    def validate(self) -> None:
        """
        Holds validation logic to be run when Django starts.
        """
        pass

    def setup(self, middleware_context) -> None:
        """
        Holds setup logic to be run once when the middleware is initialized.
        """
        pass

    def run(self, middleware_context) -> None:
        """
        Code here is executed in the middleware.
        """
        raise ImproperlyConfigured(f'The integration `{self.identifier}` is missing a `run` method')
