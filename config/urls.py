from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

from common.views import index

urlpatterns = [
    path('', index, name='root'),
    path('v1', include('v1.urls')),
    path('admin/', admin.site.urls),
]
