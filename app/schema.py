import graphene
from app.schemas import PermissionQuery, TokenQuery

class Query(
    PermissionQuery,
    TokenQuery,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query)
