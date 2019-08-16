import graphene
from app.schemas import PermissionQuery

class Query(
    PermissionQuery,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query)
