from django.conf import settings as django_settings
from django.test import override_settings

from django_guid.utils import generate_guid


def test_uuid_length():
    """
    Make sure passing uuid_length works.
    """
    for i in range(33):
        guid = generate_guid(uuid_length=i)
        assert len(guid) == i


def test_uuid_length_setting():
    """
    Make sure that the settings value is used as a default.
    """
    for i in range(33):
        mocked_settings = django_settings.DJANGO_GUID
        mocked_settings['UUID_LENGTH'] = i
        with override_settings(DJANGO_GUID=mocked_settings):
            guid = generate_guid()
            assert len(guid) == i
