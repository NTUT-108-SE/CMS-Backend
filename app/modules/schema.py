# pylint: disable=no-member
import graphene
from .database import User as UserModel
from graphene_mongo import MongoengineObjectType
from mongoengine import DoesNotExist


class User(MongoengineObjectType):
    class Meta:
        model = UserModel


class Query(graphene.ObjectType):
    user = graphene.Field(User, email=graphene.String(required=True))
    users = graphene.List(User)

    def resolve_user(self, info, email):
        try:
            return UserModel.objects.get(email=email)
        except DoesNotExist:
            return None

    def resolve_users(self, info):
        return list(UserModel.objects.all())


graphql = graphene.Schema(query=Query)