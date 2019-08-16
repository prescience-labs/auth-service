import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from app.services.jwt import JWT

class Token(graphene.ObjectType):
    token = graphene.String()

class TokenQuery(graphene.ObjectType):
    token = graphene.Field(Token)

    def resolve_token(self, info, **kwargs):
        token = JWT.encode({ 'first': 'last' })
        return TokenQuery(token=token)
