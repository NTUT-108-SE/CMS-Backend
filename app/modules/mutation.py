# pylint: disable=no-member
import graphene
from .sub_graphql.user_graphql import CreateUser, MutateUser, DeleteUser
from .sub_graphql.healthrecord_graphql import CreateHealthRecord, MutateHealthRecord, DeleteHealthRecord


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()
    mutate_user = MutateUser.Field()
    create_health_record = CreateHealthRecord.Field()
    mutate_health_record = MutateHealthRecord.Field()
    delete_health_record = DeleteHealthRecord.Field()
