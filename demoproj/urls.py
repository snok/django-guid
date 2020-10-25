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

from demoproj.views.sync_views import index_view, no_guid, rest_view
from demoproj.views.async_views import index_view as asgi_index_view

urlpatterns = [
    path('', index_view, name='index'),
    path('api', rest_view, name='drf'),
    path('no_guid', no_guid, name='no_guid'),
    path('asgi', asgi_index_view, name='asgi_index'),
]
