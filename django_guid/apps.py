from django.apps import AppConfig


class DjangoGuidConfig(AppConfig):
    name = 'django_guid'

    def ready(self) -> None:
        """
        In order to avoid circular imports we import signals here.
        """
        from django_guid import signals  # noqa F401
        from django_guid.config import settings

        settings.validate()
