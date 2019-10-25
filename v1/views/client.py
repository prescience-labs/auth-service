from django.contrib.auth import get_user_model
from rest_framework import exceptions, generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response

from common.services.auth import get_basic_auth_from_header
from v1.serializers import ClientSerializer
from common.models import Client
from ._mixins import MultipleFieldLookupMixin

class ClientFromBasicAuth(generics.RetrieveAPIView, MultipleFieldLookupMixin):
    serializer_class    = ClientSerializer
    lookup_field        = 'client_id' # necessary to avoid error with lookup_field defaults
    lookup_fields       = ('client_id', 'client_secret',)

    def get_queryset(self):
        creds = get_basic_auth_from_header(self.request)

        self.kwargs['client_id']        = creds[0]
        self.kwargs['client_secret']    = creds[1]

        return Client.objects.all().prefetch_related('permissions')
