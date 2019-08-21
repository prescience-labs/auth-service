"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
#pylint: disable=invalid-name
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from v1 import views

urlpatterns = [
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<str:uid>/', views.UserDetail.as_view(), name='user_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
