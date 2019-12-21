import graphene
import bcrypt
from datetime import datetime
from bson.objectid import ObjectId
from ..database import RegistrationModel
from mongoengine import DoesNotExist


class Registration:
    def __init__(self, registration=None, id=None, identifier=None, registration_date=None):
        if registration != None:
            self._registration = registration
        elif id != None:
            if (ObjectId.is_valid(id)):
                self._registration = RegistrationModel.objects.get(id=ObjectId(id))
            else:
                raise DoesNotExist("ID not valid!")
        elif identifier != None:
            self._registrations = RegistrationModel.objects(identifier=identifier)
        elif registration_date != None:
            self._registrations = RegistrationModel.objects(registration_date=registration_date)
        else:
            raise AttributeError(
                """
            Require one of identifier, registration, id
        """
            )

    @classmethod
    def create(cls, identifier, name, birth_date, registration_date, order):
        registration = RegistrationModel(
            identifier=identifier,
            name=name,
            birth_date=birth_date,
            registration_date=registration_date,
            order=order,
        )
        registration.save()
        registration.reload()
        return cls(registration=registration)

    @staticmethod
    def get_all():
        return list(RegistrationModel.objects.all())

    def save(self):
        self._registration.save()
        self._registration.reload()

    def delete(self):
        self._registration.delete()

    def get(self):
        return self._registration

    def update_order(self, registration):
        self._registration.update(**registration)
        self.save()

    def get_id(self):
        return str(self._registration['id'])

    def get_name(self):
        return self._registration['name']

    def is_authenticated(self):
        return True if self.get_id() is not None else False

    def is_active(self):
        return True

    def is_anonymous(self):
        return not self.is_authenticated

    def get_registration_date(self):
        return self._registration['registration_date']

    def get_order(self):
        return self._registration['order']

    def get_result(self):
        return list(self._registrations)

    def get_latest_order():
        return RegistrationModel.objects.order_by('-id').first().order

    def next():
        RegistrationModel.objects.first().delete()
        registrations = RegistrationModel.objects.all()
        return list(registrations)

    def skip():
        identifier = RegistrationModel.objects.first().identifier
        name = RegistrationModel.objects.first().name
        birth_date = RegistrationModel.objects.first().birth_date
        registration_date = RegistrationModel.objects.first().registration_date
        order = RegistrationModel.objects.order_by('-id').first().order + 1
        RegistrationModel.objects.first().delete()

        registration = RegistrationModel(
            identifier=identifier,
            name=name,
            birth_date=birth_date,
            registration_date=registration_date,
            order=order,
        )
        registration.save()
        registration.reload()
        registrations = RegistrationModel.objects.all()
        return list(registrations)
