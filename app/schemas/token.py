"""Token Schema"""
#pylint: disable=too-few-public-methods,unused-argument,no-self-use
import graphene
from app.services.jwt import JWT

class Token(graphene.ObjectType):
    """Token schema class"""
    token = graphene.String()

class TokenQuery(graphene.ObjectType):
    """Token Query
    Returns a new JWT.
    """
    token = graphene.Field(Token)

    def resolve_token(self, info, **kwargs):
        """Resolver for the `token` query."""
        token = JWT.encode({'first': 'last'})
        return TokenQuery(token=token)
