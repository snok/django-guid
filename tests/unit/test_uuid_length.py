from django.conf import settings as django_settings
from django.test import override_settings

import pytest

from django_guid.utils import generate_guid


def test_uuid_length():
    """
    Make sure passing uuid_length works.
    """
    for i in range(33):
        guid = generate_guid(uuid_length=i)
        assert len(guid) == i


@pytest.mark.parametrize('maximum_range,uuid_format,expected_type', [(33, 'hex', str), (37, 'string', str)])
def test_uuid_length_setting(maximum_range, uuid_format, expected_type):
    """
    Make sure that the settings value is used as a default.
    """
    mocked_settings = django_settings.DJANGO_GUID
    mocked_settings['UUID_FORMAT'] = uuid_format
    for uuid_lenght in range(33):
        mocked_settings['UUID_LENGTH'] = uuid_lenght
        with override_settings(DJANGO_GUID=mocked_settings):
            guid = generate_guid()
            assert isinstance(guid, expected_type)
            assert len(guid) == uuid_lenght
