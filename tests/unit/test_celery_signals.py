from copy import deepcopy

from django.conf import settings as django_settings
from django.test import override_settings

from pytest_mock import MockerFixture

from django_guid import get_guid, set_guid
from django_guid.config import Settings
from django_guid.integrations import CeleryIntegration
from django_guid.integrations.celery.context import celery_current, celery_parent
from django_guid.integrations.celery.signals import (
    clean_up,
    parent_header,
    publish_task_from_worker_or_request,
    worker_prerun,
)


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
        for correlation_id in [None, 'test', 123, -1]:
            # Set the id in our context var
            set_guid(correlation_id)

            # Run signal with empty headers
            headers = {}
            publish_task_from_worker_or_request(headers=headers)

            # Makes sure the returned headers contain the correct result
            assert headers[settings.guid_header_name] == correlation_id


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

        for correlation_id in ['test', 123, -1]:
            headers = {}
            celery_current.set(correlation_id)
            publish_task_from_worker_or_request(headers=headers)
            # Here the celery-parent-id header should exist
            assert headers[parent_header] == correlation_id


def test_worker_prerun_guid_exists(monkeypatch, mocker: MockerFixture, two_unique_uuid4):
    """
    Tests that GUID is set to the GUID if a GUID exists in the task object.
    """
    mock_task = mocker.Mock()
    mock_task.request = {'Correlation-ID': '704ae5472cae4f8daa8f2cc5a5a8mock'}
    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['INTEGRATIONS'] = [CeleryIntegration(log_parent=False)]
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.integrations.celery.signals.settings', settings)
        worker_prerun(mock_task)
    assert get_guid() == '704ae5472cae4f8daa8f2cc5a5a8mock'


def test_worker_prerun_guid_does_not_exist(monkeypatch, mocker: MockerFixture, mock_uuid):
    """
    Tests that a GUID is set if it does not exist
    """
    mock_task = mocker.Mock()
    mock_task.request = {'Correlation-ID': None}
    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['INTEGRATIONS'] = [CeleryIntegration(log_parent=False)]
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.integrations.celery.signals.settings', settings)
        worker_prerun(mock_task)
    assert get_guid() == '704ae5472cae4f8daa8f2cc5a5a8mock'


def test_worker_prerun_guid_log_parent_no_origin(monkeypatch, mocker: MockerFixture, mock_uuid_two_unique):
    """
    Tests that a GUID is set if it does not exist
    """
    from django_guid.integrations.celery.signals import parent_header

    mock_task = mocker.Mock()
    mock_task.request = {'Correlation-ID': None, parent_header: None}  # No origin
    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['INTEGRATIONS'] = [CeleryIntegration(log_parent=True)]
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.integrations.celery.signals.settings', settings)
        worker_prerun(mock_task)
    assert get_guid() == '704ae5472cae4f8daa8f2cc5a5a8mock'
    assert celery_current.get() == 'c494886651cd4baaa8654e4d24a8mock'
    assert celery_parent.get() is None


def test_worker_prerun_guid_log_parent_with_origin(monkeypatch, mocker: MockerFixture, mock_uuid_two_unique):
    """
    Tests that a GUID is set if it does not exist
    """
    from django_guid.integrations.celery.signals import parent_header

    mock_task = mocker.Mock()
    mock_task.request = {'Correlation-ID': None, parent_header: '1234'}  # No origin
    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['INTEGRATIONS'] = [CeleryIntegration(log_parent=True)]
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.integrations.celery.signals.settings', settings)
        worker_prerun(mock_task)
    assert get_guid() == '704ae5472cae4f8daa8f2cc5a5a8mock'
    assert celery_current.get() == 'c494886651cd4baaa8654e4d24a8mock'
    assert celery_parent.get() == '1234'


def test_cleanup(monkeypatch, mocker: MockerFixture):
    set_guid('123')
    celery_current.set('123')
    celery_parent.set('123')

    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['INTEGRATIONS'] = [CeleryIntegration(log_parent=True)]
    with override_settings(DJANGO_GUID=mocked_settings):
        settings = Settings()
        monkeypatch.setattr('django_guid.integrations.celery.signals.settings', settings)
        clean_up(task=mocker.Mock())

    assert [get_guid(), celery_current.get(), celery_parent.get()] == [None, None, None]
