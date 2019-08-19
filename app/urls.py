"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
#pylint: disable=invalid-name
from django.urls import include, path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from graphene_django.views import GraphQLView
from app import views

urlpatterns = [
    re_path(r'^auth/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^auth/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^auth/token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<str:uid>/', views.UserDetail.as_view(), name='user_detail'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
