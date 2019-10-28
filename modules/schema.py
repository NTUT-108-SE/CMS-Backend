# pylint: disable=no-member
import graphene
from .database import User as UserModel
from graphene_mongo import MongoengineObjectType


class User(MongoengineObjectType):
    class Meta:
        model = UserModel


class Query(graphene.ObjectType):
    user = graphene.Field(User, email=graphene.String(required=True))
    users = graphene.List(User)

    def resolve_user(self, info, email):
        return UserModel.objects.get(email=email)

    def resolve_users(self, info):
        return list(UserModel.objects.all())


schema = graphene.Schema(query=Query)
query = '''
    query {
      users {
        name
      }
    }
'''