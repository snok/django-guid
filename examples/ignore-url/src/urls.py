from django.urls import path

from . import views

urlpatterns = [
    path('ignored', views.ignored_view, name='ignored'),
]
