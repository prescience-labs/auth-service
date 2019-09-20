from django.urls import path, include
from v1 import views

urlpatterns = [
    path('/users', views.UserList.as_view(), name='user_list'),
    path('/users/<uuid:uid>', views.UserDetail.as_view(), name='user_detail'),
]
