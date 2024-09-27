"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from demoproj.views.sync_views import index_view, no_guid, rest_view, no_guid_regex
from demoproj.views.async_views import index_view as asgi_index_view
from demoproj.views.async_views import django_guid_api_usage

urlpatterns = [
    path('', index_view, name='index'),
    path('api', rest_view, name='drf'),
    path('no-guid', no_guid, name='no_guid'),
    path('no-guid-regex', no_guid_regex, name='no_guid_regex'),
    path('asgi', asgi_index_view, name='asgi_index'),
    path('api-usage', django_guid_api_usage, name='django_guid_api_usage'),
]
