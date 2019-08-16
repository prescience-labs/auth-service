"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
#pylint: disable=invalid-name
from django.urls import path
from graphene_django.views import GraphQLView

urlpatterns = [
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]
