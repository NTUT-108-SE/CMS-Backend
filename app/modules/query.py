# pylint: disable=no-member
import graphene
from .domain.user import User
from graphene_mongo import MongoengineObjectType
from mongoengine import DoesNotExist


class Result(graphene.ObjectType):
    ok = graphene.Boolean()


class Query(graphene.ObjectType):
    user = graphene.Field(User, email=graphene.String(), id=graphene.String())
    users = graphene.List(User)
    login = graphene.Field(
        Result, email=graphene.String(required=True), password=graphene.String(required=True)
    )

    def resolve_user(self, info, email=None, id=None):
        try:
            if id != None:
                return User(id=id).get()
            elif email != None:
                return User(email=email).get()
            else:
                return None
        except DoesNotExist:
            return None

    def resolve_users(self, info):
        return User.get_all()

    def resolve_login(self, info, email, password):
        try:
            user = User(email=email)
            return Result(ok=user.check_password(password))
        except Exception:
            return Result(ok=False)
