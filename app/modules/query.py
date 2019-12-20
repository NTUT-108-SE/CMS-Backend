# pylint: disable=no-member
import graphene
from .domain.user import User
from .domain.healthrecord import HealthRecord
from .domain.patient import Patient
from .domain.medication import Medication

from .sub_graphql.patient_graphql import PatientMeta, PatientsMeta
from .sub_graphql.healthrecord_graphql import HealthRecordMeta, HealthRecordsMeta
from .sub_graphql.user_graphql import UserMeta
from .sub_graphql.medication_graphql import MedicationMeta, MedicationsMeta
from graphene_mongo import MongoengineObjectType
from mongoengine import DoesNotExist


class Result(graphene.ObjectType):
    ok = graphene.Boolean()


class Query(graphene.ObjectType):
    user = graphene.Field(UserMeta, email=graphene.String(), id=graphene.String())
    users = graphene.List(UserMeta)
    login = graphene.Field(
        Result, email=graphene.String(required=True), password=graphene.String(required=True)
    )
    health_record = graphene.Field(HealthRecordMeta, id=graphene.Int(required=True))
    health_records = graphene.Field(
        HealthRecordsMeta, offset=graphene.Int(), count=graphene.Int(), patient_id=graphene.Int()
    )

    patient = graphene.Field(PatientMeta, id=graphene.Int(), identifier=graphene.String())
    patients = graphene.Field(PatientsMeta, offset=graphene.Int(), count=graphene.Int())

    medication = graphene.Field(MedicationMeta, id=graphene.Int(), name=graphene.String())
    medications = graphene.Field(MedicationsMeta, offset=graphene.Int(), count=graphene.Int())

    def resolve_user(self, info, email=None, id=None):
        try:
            if id != None:
                return User(id=id).get()
            elif email != None:
                return User(email=email).get()
            else:
                return None
        except DoesNotExist:
            return None

    def resolve_users(self, info):
        return User.get_all()

    def resolve_login(self, info, email, password):
        try:
            user = User(email=email)
            return Result(ok=user.check_password(password))
        except Exception:
            return Result(ok=False)

    def resolve_health_record(self, info, id):
        try:
            hr = HealthRecord(id=id)
            return hr
        except Exception:
            return None

    def resolve_health_records(self, info, offset=0, count=20, patient_id=None):
        try:
            hrs = None
            if patient_id == None:
                hrs = HealthRecord.get_all(offset, count)
            else:
                hrs = HealthRecord.query_patient(patient_id, offset, count)
            return hrs
        except Exception:
            return None

    def resolve_patient(self, info, id=None, identifier=None):
        try:
            patient = None
            if id != None:
                patient = Patient(id=id)
            elif identifier != None:
                patient = Patient(identifier=identifier)
            else:
                raise AttributeError("Id or Identifier must have one.")
            return patient
        except Exception:
            return None

    def resolve_patients(self, info, offset=0, count=20):
        try:
            patients = Patient.get_all(offset=offset, count=count)
            return patients
        except Exception:
            return None

    def resolve_medication(self, info, id=None):
        try:
            medication = None
            if id != None:
                medication = Medication(id=id)
            else:
                raise AttributeError("Id have one.")
            return medication
        except Exception:
            return None

    def resolve_medications(self, info, offset=0, count=20):
        try:
            medications = Medication.get_all(offset=offset, count=count)
            return medications
        except Exception:
            return None
