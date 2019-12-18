# pylint: disable=no-member
import graphene
from .sub_graphql.user_graphql import CreateUser, MutateUser, DeleteUser
from .sub_graphql.healthrecord_graphql import CreateHealthRecord, MutateHealthRecord, DeleteHealthRecord
from .sub_graphql.patient_graphql import CreatePatient, MutatePatient, DeletePatient
# from .sub_graphql.management_graphql import MutateManagement, CreateAnnouncement, MutateAnnouncement, DeleteAnnouncement


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

    # mutate_management = MutateManagement.Field()
    # create_announcement = CreateAnnouncement.Field()
    # mutate_announcement = MutateAnnouncement.Field()
    # delete_announcement = DeleteAnnouncement.Field()
