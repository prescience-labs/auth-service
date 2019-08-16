"""Schemas

Import each Query, Mutation, and Subscription schema.
"""
from .auth import AuthMutation
from .permission import PermissionQuery
from .token import TokenQuery
from .user import UserQuery, UserMutation
