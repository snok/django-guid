import pytest
from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured

from django_guid.config import Settings


def test_invalid_setting(monkeypatch):
    monkeypatch.setattr(django_settings, 'DJANGO_GUID', {'invalid_setting': 'some_value'})
    with pytest.raises(ImproperlyConfigured, match='invalid_setting is not a valid setting for django_guid'):
        Settings()


def test_invalid_guid(monkeypatch):
    monkeypatch.setattr(django_settings, 'DJANGO_GUID', {'VALIDATE_GUID': 'string'})
    with pytest.raises(ImproperlyConfigured, match='VALIDATE_GUID must be a boolean'):
        Settings()


def test_invalid_header_name(monkeypatch):
    monkeypatch.setattr(django_settings, 'DJANGO_GUID', {'GUID_HEADER_NAME': True})
    with pytest.raises(ImproperlyConfigured, match='GUID_HEADER_NAME must be a string'):
        Settings()
