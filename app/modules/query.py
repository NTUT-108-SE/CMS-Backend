# pylint: disable=no-member
import graphene
from mongoengine import DoesNotExist

from .domain.user import User
from .domain.healthrecord import HealthRecord
from .domain.patient import Patient
from .domain.management import Management
from .domain.announcement import Announcement
from .domain.medication import Medication
from .domain.invoice import Invoice
from .domain.registration import Registration

from .sub_graphql.patient_graphql import PatientMeta, PatientsMeta
from .sub_graphql.healthrecord_graphql import HealthRecordMeta, HealthRecordsMeta
from .sub_graphql.user_graphql import UserMeta
from .sub_graphql.announcement_graphql import AnnouncementMeta, AnnouncementsMeta
from .sub_graphql.management_graphql import ManagementMeta
from .sub_graphql.medication_graphql import MedicationMeta, MedicationsMeta
from .sub_graphql.invoice_graphql import InvoiceMeta, InvoicesMeta
from .sub_graphql.registration_graphql import RegistrationMeta


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

    announcement = graphene.Field(AnnouncementMeta, id=graphene.String(required=True))
    announcements = graphene.Field(AnnouncementsMeta, offset=graphene.Int(), count=graphene.Int())

    management = graphene.Field(ManagementMeta)

    medication = graphene.Field(
        MedicationMeta, id=graphene.Int(required=True), name=graphene.String()
    )
    medications = graphene.Field(MedicationsMeta, offset=graphene.Int(), count=graphene.Int())

    invoice = graphene.Field(InvoiceMeta, id=graphene.Int(required=True))
    invoices = graphene.Field(InvoicesMeta, offset=graphene.Int(), count=graphene.Int())

    registration = graphene.Field(RegistrationMeta, id=graphene.String())
    registrations = graphene.List(
        RegistrationMeta, identifier=graphene.String(), registration_date=graphene.String()
    )
    latest_order = graphene.Int(registration_date=graphene.String())

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

    def resolve_announcement(self, info, id):
        try:
            announcement = Announcement(id=id)
            return announcement.get()
        except Exception:
            return None

    def resolve_announcements(self, info, offset=0, count=20):
        try:
            announcements = Announcement.get_all(offset=offset, count=count)
            return announcements
        except Exception:
            return None

    def resolve_management(self, info):
        management = Management()
        return management.get()

    def resolve_medication(self, info, id):
        try:
            medication = Medication(id=id)
            return medication
        except Exception:
            return None

    def resolve_medications(self, info, offset=0, count=20):
        try:
            medications = Medication.get_all(offset=offset, count=count)
            return medications
        except Exception:
            return None

    def resolve_invoice(self, info, id):
        try:
            invoice = Invoice(id=id)
            return invoice
        except Exception:
            return None

    def resolve_invoices(self, info, offset=0, count=20, patient_id=None):
        try:
            invoices = None
            if patient_id == None:
                invoices = Invoice.get_all(offset=offset, count=count)
            else:
                invoices = Invoice.query_patient(patient_id, offset, count)
            return invoices
        except Exception:
            return None

    def resolve_registration(self, info, id=None):
        try:
            if id != None:
                return Registration(id=id).get()
            else:
                return None
        except DoesNotExist:
            return None

    def resolve_registrations(self, info, identifier=None, registration_date=None):
        try:
            if identifier != str(None):
                return Registration(identifier=identifier).get_result()
            elif registration_date != str(None):
                return Registration(registration_date=registration_date).get_result()
            else:
                return Registration.get_all()
        except DoesNotExist:
            return None

    def resolve_latest_order(self, info, registration_date=None):

        try:
            if registration_date != None:
                Registration(registration_date=registration_date)
                return Registration(registration_date=registration_date).get_latest_order()
            else:
                return None
        except DoesNotExist:
            return None
