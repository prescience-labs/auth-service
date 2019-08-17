"""Auth Schema"""
#pylint: disable=too-few-public-methods,unused-argument,no-self-use,no-else-return
from django.contrib.auth import authenticate
import graphene
from app.services.jwt import JWT

class AuthTokenNode(graphene.ObjectType):
    """AuthToken schema class"""
    token = graphene.String()

class AuthUserLogin(graphene.Mutation):
    """Log a user in. Returns an access token."""
    class Arguments:
        """Arguments for the authUserLogin mutation."""
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.Field(AuthTokenNode)

    @classmethod
    def mutate(cls, root, info, email, password):
        """
        Default method for Graphene Mutation.
        Do not rename.
        """
        user = authenticate(
            username=email,
            password=password
        )
        if user is None:
            token = JWT.get_user_token(user)
            return AuthUserLogin({'token':token})
        else:
            raise Exception('User authentication failed.')

class AuthMutation(graphene.ObjectType):
    """GraphQL mutations for Authentication/Authorization."""
    auth_user_login = AuthUserLogin.Field()
