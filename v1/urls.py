from django.urls import path, include
import oauth2_provider.views as oauth2_views
from rest_framework.urlpatterns import format_suffix_patterns
from v1 import views

oauth2_endpoint_views = [
    path('/authorize',      oauth2_views.AuthorizationView.as_view(),   name='authorize'),
    path('/token',          oauth2_views.TokenView.as_view(),           name='token'),
    path('/revoke-token',   oauth2_views.RevokeTokenView.as_view(),     name='revoke-token'),
    path('/introspect',     oauth2_views.IntrospectTokenView.as_view(), name='introspect'),
]

urlpatterns = [
    # path('/auth/token', views.token_obtain, name='auth_token_obtain'),
    # path('/auth/token/refresh', views.token_refresh, name='auth_token_refresh'),
    # path('/auth/token/verify', views.token_verify, name='auth_token_verify'),
    # path('/auth/current_user', views.CurrentUser.as_view(), name='current_user'),
    # path('/auth/password_reset', views.AuthPasswordResetInit.as_view(), name='password_reset'),
    # path('/auth/password_reset/submit', views.AuthPasswordResetFinal.as_view(), name='password_reset_final'),

    path('/auth',               include(oauth2_endpoint_views)),
    path('/auth/login',         views.login, name='auth_login'),
    path('/users',              views.UserList.as_view(), name='user_list'),
    path('/users/<uuid:uid>',   views.UserDetail.as_view(), name='user_detail'),
]
