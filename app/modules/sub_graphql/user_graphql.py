import graphene
from ..domain.User import User


class UserInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    name = graphene.String(required=True)
    password = graphene.String(required=True)
    image = graphene.String()
    introduction = graphene.String()
    role = graphene.String(required=True)


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(User)

    @staticmethod
    def mutate(root, info, user_data):
        try:
            user = User.create(**user_data)
            return CreateUser(user=user.get(), ok=True)
        except Exception:
            return CreateUser(user=None, ok=False)


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