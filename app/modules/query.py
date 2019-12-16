# pylint: disable=no-member
import graphene
from .domain.user import User
from .domain.healthrecord import HealthRecord
from .sub_graphql.healthrecord_graphql import HealthRecordMeta, HealthRecordsMeta
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
    health_record = graphene.Field(HealthRecordMeta, id=graphene.Int(required=True))
    health_records = graphene.Field(HealthRecordsMeta, offset=graphene.Int(), count=graphene.Int())

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

    def resolve_health_record(self, info, id):
        try:
            hr = HealthRecord(id=id)
            return hr
        except Exception:
            return None

    def resolve_health_records(self, info, offset=0, count=20):
        try:
            hrs = HealthRecord.get_all(offset, count)
            return hrs
        except Exception:
            return None