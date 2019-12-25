import graphene
from graphene_mongo import MongoengineObjectType
from ..domain.user import User
from ..database import UserModel


class UserMeta(MongoengineObjectType):
    class Meta:
        model = UserModel


class UserInput(graphene.InputObjectType):
    email = graphene.String()
    id = graphene.String()
    name = graphene.String()
    password = graphene.String()
    image = graphene.String()
    introduction = graphene.String()
    role = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserMeta)

    @staticmethod
    def mutate(root, info, user_data):
        try:
            user = User.create(**user_data)
            return CreateUser(user=user.get(), ok=True)
        except Exception:
            return CreateUser(user=None, ok=False)


class MutateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserMeta)

    @staticmethod
    def mutate(root, info, user_data):
        try:
            user = User(email=user_data.email) if user_data.email else User(id=user_data.id)
            if user_data.role:
                user.update_role(user_data.role)
            elif user_data.password:
                user.update_password(user_data.password)
            else:
                user.update(user_data)
            return MutateUser(user=user.get(), ok=True)
        except Exception:
            return MutateUser(user=None, ok=False)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        email = graphene.String()

    ok = graphene.Boolean()

    def mutate(root, info, id=None, email=None):
        try:
            if id != None:
                User(id=id).delete()
            elif email != None:
                User(email=email).delete()
            else:
                raise AttributeError("At least one attribute should be assigned!")

            ok = True
            return DeleteUser(ok=ok)
        except Exception:
            return DeleteUser(ok=False)
