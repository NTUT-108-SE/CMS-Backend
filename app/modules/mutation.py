# pylint: disable=no-member
import graphene
from .sub_graphql.user_graphql import CreateUser, MutateUser, DeleteUser
from .sub_graphql.healthrecord_graphql import CreateHealthRecord, MutateHealthRecord, DeleteHealthRecord
from .sub_graphql.patient_graphql import CreatePatient, MutatePatient, DeletePatient
from .sub_graphql.medication_graphql import CreateMedication, MutateMedication, DeleteMedication


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()
    mutate_user = MutateUser.Field()

    create_health_record = CreateHealthRecord.Field()
    mutate_health_record = MutateHealthRecord.Field()
    delete_health_record = DeleteHealthRecord.Field()

    create_patient = CreatePatient.Field()
    mutate_patient = MutatePatient.Field()
    delete_patient = DeletePatient.Field()

    create_medication = CreateMedication.Field()
    mutate_medication = MutateMedication.Field()
    delete_medication = DeleteMedication.Field()
