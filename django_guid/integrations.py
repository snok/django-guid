import logging

from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger('django_guid')


class SentryIntegration:
    def __init__(self):
        """
        Run when integration is initialized in the clients settings.py.

        Makes sure the client has installed the `sentry_sdk` package, and that the header is appropriately named.
        """
        try:
            import sentry_sdk  # noqa: F401
        except ModuleNotFoundError:
            raise ImproperlyConfigured(
                'The package `sentry-sdk` is required for integrating with Sentry. '
                'Please run `pip install sentry-sdk`, or set `INTEGRATE_SENTRY` to False in the DJANGO_GUID settings.'
            )

    @staticmethod
    def run(self):
        """
        Section run in the middleware
        """
        import sentry_sdk

        with sentry_sdk.configure_scope() as scope:
            guid = self.get_guid()
            logger.debug('Setting Sentry transaction_id to %s', guid)
            scope.set_tag('transaction_id', guid)
