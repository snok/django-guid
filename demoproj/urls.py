from django.urls import path

from demoproj.views.sync_views import index_view, no_guid, rest_view
from demoproj.views.async_views import index_view as asgi_index_view
from demoproj.views.async_views import django_guid_api_usage

urlpatterns = [
    path('', index_view, name='index'),
    path('api', rest_view, name='drf'),
    path('no-guid', no_guid, name='no_guid'),
    path('asgi', asgi_index_view, name='asgi_index'),
    path('api-usage', django_guid_api_usage, name='django_guid_api_usage'),
]
