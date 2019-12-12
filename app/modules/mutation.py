# pylint: disable=no-member
import graphene
from .sub_graphql.user_graphql import CreateUser, MutateUser, DeleteUser


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()
    mutate_user = MutateUser.Field()