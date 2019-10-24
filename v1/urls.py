from django.urls import path, include
from v1 import views

urlpatterns = [
    path('/teams', views.TeamList.as_view(), name='team_list'),
    path('/teams/<uuid:pk>', views.TeamDetail.as_view(), name='team_detail'),

    path('/users', views.UserList.as_view(), name='users'),
    path('/users/<uuid:pk>', views.UserDetail.as_view(), name='user_detail'),

    path('/token', views.TokenObtainView.as_view(), name='token_obtain'),
    path('/token/refresh', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('/token/verify', views.TokenVerifyView.as_view(), name='token_verify'),
    path('/token/force', views.ForceTokenObtainView.as_view(), name='force_token_obtain'),
    path('/token/user', views.UserFromTokenDetail.as_view(), name='user_from_token'),
]
