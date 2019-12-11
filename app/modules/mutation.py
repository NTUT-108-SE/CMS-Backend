# pylint: disable=no-member
import graphene
from .sub_graphql.user_graphql import CreateUser, DeleteUser


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()