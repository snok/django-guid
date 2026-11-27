import warnings

import pytest
from asgiref.sync import iscoroutinefunction, markcoroutinefunction

from django_guid.middleware import guid_middleware


def sync_get_response(request):
    return None


async def async_get_response(request):
    return None


def marked_get_response(request):
    return None


markcoroutinefunction(marked_get_response)


@pytest.mark.parametrize(
    ('get_response', 'is_async'),
    [(sync_get_response, False), (async_get_response, True), (marked_get_response, True)],
)
def test_middleware_matches_get_response(get_response, is_async):
    """
    The middleware is async when get_response is, including a callable marked with asgiref's markcoroutinefunction,
    which inspect.iscoroutinefunction only recognizes from Python 3.12.
    """
    assert iscoroutinefunction(guid_middleware(get_response)) == is_async


@pytest.mark.parametrize('get_response', [sync_get_response, async_get_response])
def test_no_deprecation_warning(get_response):
    """
    Creating the middleware raises no DeprecationWarning (asyncio.iscoroutinefunction is deprecated from Python 3.14).
    """
    with warnings.catch_warnings():
        warnings.simplefilter('error', DeprecationWarning)
        guid_middleware(get_response)
