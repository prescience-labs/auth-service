from rest_framework import serializers
from app.services.jwt import JWT

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(read_only=True)

    def create(self, user):
        self.token = JWT.get_user_token(user)
        return self
