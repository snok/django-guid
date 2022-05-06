import uuid

import pytest


@pytest.fixture
def mock_uuid(monkeypatch):
    class MockUUid:
        hex = '704ae5472cae4f8daa8f2cc5a5a8mock'

        def __str__(self):
            return f'{self.hex[:8]}-{self.hex[8:12]}-{self.hex[12:16]}-{self.hex[16:20]}-{self.hex[20:]}'

    monkeypatch.setattr('django_guid.utils.uuid.uuid4', MockUUid)


@pytest.fixture
def two_unique_uuid4():
    return ['704ae5472cae4f8daa8f2cc5a5a8mock', 'c494886651cd4baaa8654e4d24a8mock']


@pytest.fixture
def mock_uuid_two_unique(mocker, two_unique_uuid4):
    mocker.patch.object(
        uuid.UUID,
        'hex',
        new_callable=mocker.PropertyMock,
        side_effect=two_unique_uuid4,
    )


@pytest.fixture(autouse=True)
def integrations(settings):
    settings.DJANGO_GUID['INTEGRATIONS'] = []
