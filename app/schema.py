"""App GraphQL Schema

This schema combines all other schemas from app.schemas
into one application-global GraphQL schema.
"""
#pylint: disable=unnecessary-pass,too-few-public-methods
import graphene
from app.schemas import PermissionQuery, TokenQuery, UserQuery, UserMutation

class Query(
        PermissionQuery,
        TokenQuery,
        UserQuery,
        graphene.ObjectType,
):
    """
    All application query schemas.
    """
    pass

class Mutation(
        UserMutation,
        graphene.ObjectType,
):
    """
    All application mutation schemas.
    """
    pass

SCHEMA = graphene.Schema(query=Query, mutation=Mutation)
