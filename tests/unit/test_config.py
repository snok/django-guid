from copy import deepcopy

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

import pytest

from django_guid.config import Settings


@override_settings()
def test_no_config(settings):
    del settings.DJANGO_GUID
    Settings().validate()


def test_invalid_guid():
    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['VALIDATE_GUID'] = 'string'
    with override_settings(DJANGO_GUID=mocked_settings):
        with pytest.raises(ImproperlyConfigured, match='VALIDATE_GUID must be a boolean'):
            Settings().validate()


def test_invalid_header_name():
    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['GUID_HEADER_NAME'] = True
    with override_settings(DJANGO_GUID=mocked_settings):
        with pytest.raises(ImproperlyConfigured, match='GUID_HEADER_NAME must be a string'):
            Settings().validate()


def test_invalid_return_header_setting():
    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['RETURN_HEADER'] = 'string'
    with override_settings(DJANGO_GUID=mocked_settings):
        with pytest.raises(ImproperlyConfigured, match='RETURN_HEADER must be a boolean'):
            Settings().validate()


def test_invalid_expose_header_setting():
    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['EXPOSE_HEADER'] = 'string'
    with override_settings(DJANGO_GUID=mocked_settings):
        with pytest.raises(ImproperlyConfigured, match='EXPOSE_HEADER must be a boolean'):
            Settings().validate()


def test_valid_settings():
    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['VALIDATE_GUID'] = False
    mocked_settings['GUID_HEADER_NAME'] = 'Correlation-ID-TEST'
    mocked_settings['RETURN_HEADER'] = False
    mocked_settings['EXPOSE_HEADER'] = False
    with override_settings(DJANGO_GUID=mocked_settings):
        assert not Settings().validate_guid
        assert Settings().guid_header_name == 'Correlation-ID-TEST'
        assert not Settings().return_header


def test_bad_integrations_type():
    for setting in [{}, '', 2, None, -2]:
        mocked_settings = deepcopy(django_settings.DJANGO_GUID)
        mocked_settings['INTEGRATIONS'] = setting
        with override_settings(DJANGO_GUID=mocked_settings):
            with pytest.raises(ImproperlyConfigured, match='INTEGRATIONS must be an array'):
                Settings().validate()


def test_not_array_ignore_urls():
    for setting in [{}, '', 2, None, -2]:
        mocked_settings = deepcopy(django_settings.DJANGO_GUID)
        mocked_settings['IGNORE_URLS'] = setting
        with override_settings(DJANGO_GUID=mocked_settings):
            with pytest.raises(ImproperlyConfigured, match='IGNORE_URLS must be an array'):
                Settings().validate()


def test_not_string_in_igore_urls():
    for setting in ['api/v1/test', 'api/v1/othertest', True], [1, 2, 'yup']:
        mocked_settings = deepcopy(django_settings.DJANGO_GUID)
        mocked_settings['IGNORE_URLS'] = setting
        with override_settings(DJANGO_GUID=mocked_settings):
            with pytest.raises(ImproperlyConfigured, match='IGNORE_URLS must be an array of strings'):
                Settings().validate()


def test_uuid_len_fail():
    for setting in [True, False, {}, [], 'asd', -1, 0, 33]:
        mocked_settings = deepcopy(django_settings.DJANGO_GUID)
        mocked_settings['UUID_LENGTH'] = setting
        with override_settings(DJANGO_GUID=mocked_settings):
            with pytest.raises(ImproperlyConfigured, match='UUID_LENGTH must be an integer and be between 1-32'):
                Settings().validate()


def test_converts_correctly():
    mocked_settings = deepcopy(django_settings.DJANGO_GUID)
    mocked_settings['IGNORE_URLS'] = ['/no-guid', '/my/api/path/']
    with override_settings(DJANGO_GUID=mocked_settings):
        assert 'my/api/path' in Settings().ignore_urls
        assert 'no-guid' in Settings().ignore_urls
