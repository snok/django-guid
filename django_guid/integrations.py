import logging

from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger('django_guid')


class SentryIntegration:
    """
    This integrations, when added to the django_guid settings,
    ensures that each requests correlation ID is passed on to Sentry exception logs.
    """

    def __init__(self):
        """
        This is run when the integration is initialized in the clients settings.py.

        Put all validation logic here.
        """
        # Makes sure the client has installed the `sentry_sdk` package, and that the header is appropriately named.
        try:
            import sentry_sdk  # noqa: F401
        except ModuleNotFoundError:
            raise ImproperlyConfigured(
                'The package `sentry-sdk` is required for extending your tracing IDs to Sentry. '
                'Please run `pip install sentry-sdk` if you wish to include this integration.'
            )

    @staticmethod
    def run(self):
        """
        This method holds execution logic to be executed in the middleware.
        """
        import sentry_sdk

        with sentry_sdk.configure_scope() as scope:
            guid = self.get_guid()
            logger.debug('Setting Sentry transaction_id to %s', guid)
            scope.set_tag('transaction_id', guid)
