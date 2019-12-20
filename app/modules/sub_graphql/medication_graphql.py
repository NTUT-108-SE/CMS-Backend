import graphene
from ..domain.medication import Medication


class MedicationMeta(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    synonym = graphene.String()
    ingredient = graphene.String()
    contraindication = graphene.String()
    dosage = graphene.String()
    patient_characteristics = graphene.String()


class MedicationsMeta(graphene.ObjectType):
    total = graphene.Int()
    entry = graphene.List(MedicationMeta)
    offset = graphene.Int()
    count = graphene.Int()


class MedicationInput(graphene.InputObjectType):
    name = graphene.String()
    synonym = graphene.String()
    ingredient = graphene.String()
    contraindication = graphene.String()
    dosage = graphene.String()
    patient_characteristics = graphene.String()


class CreateMedication(graphene.Mutation):
    class Arguments:
        medication_data = MedicationInput(required=True)

    ok = graphene.Boolean()
    medication = graphene.Field(MedicationMeta)

    @staticmethod
    def mutate(root, info, medication_data):
        try:
            medication = Medication.create(**medication_data)

            return CreateMedication(medication=medication, ok=True)
        except Exception:

            return CreateMedication(medication=None, ok=False)


class MutateMedication(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        medication_data = MedicationInput(required=True)

    ok = graphene.Boolean()
    medication = graphene.Field(MedicationMeta)

    @staticmethod
    def mutate(root, info, id, medication_data):
        try:
            medication = Medication(id)
            medication.update(**medication_data)
            return MutateMedication(medication=medication, ok=True)
        except Exception:
            return MutateMedication(medication=None, ok=False)


class DeleteMedication(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, id):
        try:
            Medication(id).delete()
            ok = True
            return DeleteMedication(ok=ok)
        except Exception:
            return DeleteMedication(ok=False)
