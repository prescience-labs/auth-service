"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
#pylint: disable=invalid-name
from django.urls import include, path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view
from app import views

schema_view = get_swagger_view(title='Auth Service')

urlpatterns = [
    path('', schema_view),

    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<str:uid>/', views.UserDetail.as_view(), name='user_detail'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
