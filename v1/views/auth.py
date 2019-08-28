from rest_framework import exceptions, generics, mixins, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from v1.serializers import PasswordResetInitSerializer, PasswordResetCompleteSerializer

User = get_user_model()

class AuthPasswordResetInit(generics.CreateAPIView):
    serializer_class = PasswordResetInitSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.NotFound:
            raise exceptions.NotFound(f"We couldn't find the user with the email {request.data['email']}")
        except:
            raise exceptions.APIException("We couldn't send the password reset email. Please reach out to us directly!")
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class AuthPasswordResetFinal(generics.UpdateAPIView):
    serializer_class    = PasswordResetCompleteSerializer
    queryset            = User.objects.all()
    lookup_field        = 'password_reset_token'

    def patch(self, request, *args, **kwargs):
        try:
            data = dict(request.data)
            data['token'] = str(kwargs['password_reset_token'])
            print(data)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
        except exceptions.NotFound:
            raise exceptions.NotFound("That password reset token wasn't valid.")
        except:
            raise exceptions.NotAcceptable("That password reset token wasn't valid.")
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
