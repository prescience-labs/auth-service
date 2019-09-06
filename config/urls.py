"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
#pylint: disable=invalid-name
from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Auth Service')

urlpatterns = [
    path('',        schema_view),
    path('v1',      include('v1.urls')),
    path('admin/',  admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
