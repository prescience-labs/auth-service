"""Auth Schema"""
#pylint: disable=too-few-public-methods,unused-argument,no-self-use
from django.contrib.auth.models import User
import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

class UserNode(DjangoObjectType):
    """The Graphene Relay node for the User model.
    https://docs.graphene-python.org/en/latest/relay/nodes/
    """
    class Meta:
        """The Meta class for UserNode.
        https://docs.graphene-python.org/projects/django/en/latest/tutorial-relay/#schema
        """
        model = User
        fields = ('username', 'email')
        filter_fields = {
            'username': ['exact', 'icontains', 'istartswith'],
            'email': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )

class UserQuery(graphene.ObjectType):
    """The GraphQL query for the User resource."""
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    def resolve_user(self, info, user_id):
        """Resolves the `user(id: ID!)` query."""
        return User.objects.get(pk=user_id)

    def resolve_users(self, info, **kwargs):
        """Resolves the `users` query."""
        return User.objects.all()

class CreateUser(relay.ClientIDMutation):
    """Create a new user. Returns the new user."""
    class Input:
        """Arguments for the createUser mutation."""
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, email, password):
        """
        Default method for Graphene Relay.
        Do not rename.
        """
        user = User.objects.create(
            email=email,
            username=email,
        )
        user.set_password(password)
        user.save()
        return CreateUser(user)

class UserMutation(graphene.ObjectType):
    """GraphQL mutations for the User resource."""
    create_user = CreateUser.Field()
