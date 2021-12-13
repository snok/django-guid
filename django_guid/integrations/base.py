from typing import Any, Optional

from django.core.exceptions import ImproperlyConfigured


class Integration:
    """
    Integration base class.
    """

    identifier: Optional[str] = None  # The name of your integration

    def __init__(self) -> None:
        if self.identifier is None:
            raise ImproperlyConfigured('`identifier` cannot be None')

    def setup(self) -> None:
        """
        Holds validation and setup logic to be run when Django starts.
        """
        pass

    def run(self, guid: str, **kwargs: Any) -> None:
        """
        Code here is executed in the middleware, before the view is called.
        """
        raise ImproperlyConfigured(f'The integration `{self.identifier}` is missing a `run` method')

    def cleanup(self, **kwargs: Any) -> None:
        """
        Code here is executed in the middleware, after the view is called.
        """
        pass
