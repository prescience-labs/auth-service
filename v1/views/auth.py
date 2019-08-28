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
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

class AuthPasswordResetFinal(generics.UpdateAPIView):
    serializer_class    = PasswordResetCompleteSerializer
    queryset            = User.objects.all()
    lookup_field        = 'password_reset_token'

    def update(self, request, *args, **kwargs):
        print(request.data)
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError:
            exceptions.ValidationError("We couldn't validate the data you sent. Is it formatted correctly and are all of the required fields included?")
        except exceptions.NotFound:
            raise exceptions.NotFound("That password reset token wasn't valid. It may have expired or never have existed.")
        except:
            raise exceptions.NotAcceptable("That password reset token wasn't valid. It may have expired or never have existed.")
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
