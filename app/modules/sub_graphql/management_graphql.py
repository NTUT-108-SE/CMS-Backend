import graphene
from ..domain.management import Management
from graphene_mongo import MongoengineObjectType
from ..database import ManagementModel


class ManagementMeta(MongoengineObjectType):
    class Meta:
        model = ManagementModel


class ManagementInput(graphene.InputObjectType):
    images = graphene.List(graphene.String)
    URLs = graphene.List(graphene.String)
    title = graphene.String()
    time = graphene.String()
    description = graphene.String()
    our_services = graphene.String()
    doctor_description = graphene.String()
    clinic_address = graphene.String()


class MutateManagement(graphene.Mutation):
    class Arguments:
        management_data = ManagementInput(required=True)

    ok = graphene.Boolean()
    management = graphene.Field(ManagementMeta)

    @staticmethod
    def mutate(root, info, management_data):
        try:
            management = Management()
            management.update(management_data)
            return MutateManagement(ok=True, management=management.get())
        except Exception:
            return MutateManagement(ok=False, management=None)
