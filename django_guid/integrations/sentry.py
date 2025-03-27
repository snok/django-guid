import logging
from typing import Any

from django.core.exceptions import ImproperlyConfigured

from django_guid.integrations import Integration

logger = logging.getLogger('django_guid')


class SentryIntegration(Integration):
    """
    Ensures that each request's correlation ID is passed on to Sentry exception logs as a `transaction_id`.
    """

    identifier = 'SentryIntegration'

    def setup(self) -> None:
        """
        Verifies that the sentry_sdk dependency is installed.
        """
        # Makes sure the client has installed the `sentry_sdk` package, and that the header is appropriately named.
        try:
            import sentry_sdk  # noqa: F401
        except ModuleNotFoundError:
            raise ImproperlyConfigured(
                'The package `sentry-sdk` is required for extending your tracing IDs to Sentry. '
                'Please run `pip install sentry-sdk` if you wish to include this integration.'
            )

    def run(self, guid: str, **kwargs: Any) -> None:
        """
        Sets the Sentry transaction_id.
        """
        import sentry_sdk
        from packaging import version

        if version.parse(sentry_sdk.VERSION) >= version.parse('2.12.0'):
            with sentry_sdk.isolation_scope() as scope:
                scope.set_tag('transaction_id', guid)
        else:
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag('transaction_id', guid)

        logger.debug('Setting Sentry transaction_id to %s', guid)
