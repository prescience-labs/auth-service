"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
#pylint: disable=invalid-name
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from v1 import views

urlpatterns = [
    path('auth/token/', views.token_obtain, name='auth_token_obtain'),
    path('auth/token/refresh/', views.token_refresh, name='auth_token_refresh'),
    path('auth/token/verify/', views.token_verify, name='auth_token_verify'),

    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/current_user/', views.CurrentUser.as_view(), name='current_user'),
    path('users/<str:uid>/', views.UserDetail.as_view(), name='user_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
