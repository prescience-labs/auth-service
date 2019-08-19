"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
#pylint: disable=invalid-name
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from graphene_django.views import GraphQLView
from app import views

urlpatterns = [
    path('auth/token/', views.Token.as_view(), name='auth_token'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<str:uid>/', views.UserDetail.as_view(), name='user_detail'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
