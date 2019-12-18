import graphene
from ..domain.patient import Patient


class PatientMeta(graphene.ObjectType):
    id = graphene.Int()
    identifier = graphene.String()
    family = graphene.String()
    given = graphene.String()
    phone = graphene.String()
    gender = graphene.String()
    birth_date = graphene.String()
    address = graphene.String()
    marital_status = graphene.String()


class PatientsMeta(graphene.ObjectType):
    total = graphene.Int()
    entry = graphene.List(PatientMeta)
    offset = graphene.Int()
    count = graphene.Int()


class PatientInput(graphene.InputObjectType):
    identifier = graphene.String()
    family = graphene.String()
    given = graphene.String()
    phone = graphene.String()
    gender = graphene.String()
    birth_date = graphene.String()
    address = graphene.String()
    marital_status = graphene.String()


class CreatePatient(graphene.Mutation):
    class Arguments:
        patient_data = PatientInput(required=True)

    ok = graphene.Boolean()
    patient = graphene.Field(PatientMeta)

    @staticmethod
    def mutate(root, info, patient_data):
        try:
            patient = Patient.create(**patient_data)
            return CreatePatient(patient=patient, ok=True)
        except Exception:
            return CreatePatient(patient=None, ok=False)


class MutatePatient(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        identifier = graphene.String()
        patient_data = PatientInput(required=True)

    ok = graphene.Boolean()
    patient = graphene.Field(PatientMeta)

    @staticmethod
    def mutate(root, info, patient_data, id=None, identifier=None):
        try:
            patient = None
            if id != None:
                patient = Patient(id=id)
            elif identifier != None:
                patient = Patient(identifier=identifier)
            else:
                raise AttributeError("Id or Identifier must have one.")
            patient.update(**patient_data)
            return MutatePatient(patient=patient, ok=True)
        except Exception:
            return MutatePatient(patient=None, ok=False)


class DeletePatient(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        identifier = graphene.String()

    ok = graphene.Boolean()

    def mutate(root, info, id=None, identifier=None):
        try:
            if id != None:
                Patient(id=id).delete()
            elif identifier != None:
                Patient(identifier=identifier).delete()
            else:
                raise AttributeError("Id or Identifier must have one.")
            ok = True
            return DeletePatient(ok=ok)
        except Exception:
            return DeletePatient(ok=False)
