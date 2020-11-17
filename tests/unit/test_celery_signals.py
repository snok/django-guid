from copy import deepcopy

from django.conf import settings as django_settings
from django.test import override_settings

from django_guid import set_guid
from django_guid.config import Settings, settings
from django_guid.integrations import CeleryIntegration
from django_guid.integrations.celery.context import celery_current
from django_guid.integrations.celery.signals import parent_header, publish_task_from_worker_or_request


def test_task_publish_includes_correct_headers(monkeypatch):
    """
    It's important that we include the correct headers when publishing a task
    to the celery worker pool, otherwise there's no transfer of state.
    """
    # Mocking overhead
    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['INTEGRATIONS'] = [CeleryIntegration(log_parent=False)]
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.integrations.celery.signals.settings', settings)

        # Actual testing
        for id in [None, 'test', 123, -1]:
            # Set the id in our context var
            set_guid(id)

            # Run signal with empty headers
            headers = {}
            publish_task_from_worker_or_request(headers=headers)

            # Makes sure the returned headers contain the correct result
            assert headers[settings.guid_header_name] == id


def test_task_publish_includes_correct_depth_headers(monkeypatch):
    """
    Test log_parent True
    """
    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['INTEGRATIONS'] = [CeleryIntegration(log_parent=True)]
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.integrations.celery.signals.settings', settings)

        headers = {}
        publish_task_from_worker_or_request(headers=headers)
        # The parent header should not be in headers, because
        # There should be no celery_current context
        assert parent_header not in headers

        for id in ['test', 123, -1]:
            headers = {}
            celery_current.set(id)
            publish_task_from_worker_or_request(headers=headers)
            # Here the celery-parent-id header should exist
            assert headers[parent_header] == id
