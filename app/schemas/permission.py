import graphene
from django.contrib.auth.models import Permission
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

class PermissionNode(DjangoObjectType):
    """The Graphene Relay node for the Permission model.
    https://docs.graphene-python.org/en/latest/relay/nodes/
    """
    class Meta:
        """The Meta class for PermissionNode.
        https://docs.graphene-python.org/projects/django/en/latest/tutorial-relay/#schema
        """
        model = Permission
        fields = ('name', 'codename')
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'codename': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )

class PermissionQuery(graphene.ObjectType):
    """The GraphQL query."""
    permission = relay.Node.Field(PermissionNode)
    permissions = DjangoFilterConnectionField(PermissionNode)

    def resolve_permission(self, info, review_id):
        """Resolves the `permission(id: ID!)` query."""
        return Permission.objects.get(pk=review_id)

    def resolve_permissions(self, info, **kwargs):
        """Resolves the `permissions` query."""
        return Permission.objects.all()
