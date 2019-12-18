import graphene
from ..domain.healthrecord import HealthRecord


class HealthRecordMeta(graphene.ObjectType):
    id = graphene.Int()
    patient_id = graphene.Int()
    code = graphene.String()
    medication = graphene.String()
    date = graphene.String()
    identifier = graphene.String()
    name = graphene.String()


class HealthRecordsMeta(graphene.ObjectType):
    total = graphene.Int()
    entry = graphene.List(HealthRecordMeta)
    offset = graphene.Int()
    count = graphene.Int()


class HealthRecordInput(graphene.InputObjectType):
    patient_id = graphene.Int()
    code = graphene.String()
    medication = graphene.String()
    date = graphene.String()
    identifier = graphene.String()
    name = graphene.String()


class CreateHealthRecord(graphene.Mutation):
    class Arguments:
        health_record_data = HealthRecordInput(required=True)

    ok = graphene.Boolean()
    health_record = graphene.Field(HealthRecordMeta)

    @staticmethod
    def mutate(root, info, health_record_data):
        try:
            hr = HealthRecord.create(**health_record_data)
            return CreateHealthRecord(health_record=hr, ok=True)
        except Exception:
            return CreateHealthRecord(health_record=None, ok=False)


class MutateHealthRecord(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        health_record_data = HealthRecordInput(required=True)

    ok = graphene.Boolean()
    health_record = graphene.Field(HealthRecordMeta)

    @staticmethod
    def mutate(root, info, id, health_record_data):
        try:
            hr = HealthRecord(id)
            hr.update(**health_record_data)
            return MutateHealthRecord(health_record=hr, ok=True)
        except Exception:
            return MutateHealthRecord(health_record=None, ok=False)


class DeleteHealthRecord(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(root, info, id):
        try:
            HealthRecord(id).delete()
            ok = True
            return DeleteHealthRecord(ok=ok)
        except Exception:
            return DeleteHealthRecord(ok=False)
