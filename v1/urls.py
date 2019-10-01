from django.urls import path, include
from v1 import views

urlpatterns = [
    path('/teams', views.TeamList.as_view(), name='team_list'),
    path('/teams/<uuid:pk>', views.TeamDetail.as_view(), name='team_detail'),
    # path('/users', views.Users.as_view(), name='users'),
    # path('/users/<uuid:uid>', views.UserDetail.as_view(), name='user_detail'),
]
