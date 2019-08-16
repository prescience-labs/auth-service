"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
#pylint: disable=invalid-name
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
]
