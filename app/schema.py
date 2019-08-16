"""App GraphQL Schema

This schema combines all other schemas from app.schemas
into one application-global GraphQL schema.
"""
#pylint: disable=unnecessary-pass
import graphene
from app.schemas import PermissionQuery, TokenQuery

class Query(
        PermissionQuery,
        TokenQuery,
        graphene.ObjectType,
):
    """
    All application query schemas.
    """
    pass

SCHEMA = graphene.Schema(query=Query)
