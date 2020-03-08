import logging

from django.core.exceptions import ImproperlyConfigured

from django_guid.integrations import Integration

logger = logging.getLogger('django_guid')


class SentryIntegration(Integration):
    """
    Ensures that each request's correlation ID is passed on to Sentry exception logs as a `transaction_id`.
    """

    identifier = 'Sentry'

    def __init__(self) -> None:
        """
        Holds validation logic run on initialization.
        """
        super().__init__()
        # Makes sure the client has installed the `sentry_sdk` package, and that the header is appropriately named.
        try:
            import sentry_sdk  # noqa: F401
        except ModuleNotFoundError:
            raise ImproperlyConfigured(
                'The package `sentry-sdk` is required for extending your tracing IDs to Sentry. '
                'Please run `pip install sentry-sdk` if you wish to include this integration.'
            )

    def run(self, middleware_context) -> None:
        import sentry_sdk
        with sentry_sdk.configure_scope() as scope:
            guid = middleware_context.get_guid()
            logger.debug('Setting Sentry transaction_id to %s', guid)
            scope.set_tag('transaction_id', guid)
