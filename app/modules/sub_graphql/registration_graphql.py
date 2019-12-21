import graphene
from graphene_mongo import MongoengineObjectType
from ..domain.registration import Registration
from ..database import RegistrationModel


class RegistrationMeta(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    identifier = graphene.String()
    registration_date = graphene.String()
    birth_date = graphene.String()
    order = graphene.Int()


class RegistrationInput(graphene.InputObjectType):
    id = graphene.String()
    identifier = graphene.String()
    name = graphene.String()
    birth_date = graphene.String()
    registration_date = graphene.String()
    order = graphene.String()


class CreateRegistration(graphene.Mutation):
    class Arguments:
        registration_data = RegistrationInput(required=True)

    ok = graphene.Boolean()
    registration = graphene.Field(RegistrationMeta)

    @staticmethod
    def mutate(root, info, registration_data):

        try:
            registration = Registration.create(**registration_data)
            return CreateRegistration(registration=registration.get(), ok=True)
        except Exception:
            return CreateRegistration(registration=None, ok=False)


class DeleteRegistration(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        identifier = graphene.String()

    ok = graphene.Boolean()

    def mutate(root, info, id=None, identifier=None):
        try:
            if id != None:
                Registration(id=id).delete()
            elif identifier != None:
                Registration(identifier=identifier).delete()
            else:
                raise AttributeError("At least one attribute should be assigned!")

            ok = True
            return DeleteRegistration(ok=ok)
        except Exception:
            return DeleteRegistration(ok=False)


class SkipRegistration(graphene.Mutation):
    ok = graphene.Boolean()
    registrations = graphene.List(RegistrationMeta)

    def mutate(root, info):
        try:
            registrations = Registration.skip()
            ok = True
            return SkipRegistration(ok=ok, registrations=registrations)
        except Exception:
            return SkipRegistration(ok=False, registrations=None)


class NextRegistration(graphene.Mutation):
    ok = graphene.Boolean()
    registrations = graphene.List(RegistrationMeta)

    def mutate(root, info):
        try:
            registrations = Registration.next()
            ok = True
            return SkipRegistration(ok=ok, registrations=registrations)
        except Exception:
            return SkipRegistration(ok=False, registrations=None)
