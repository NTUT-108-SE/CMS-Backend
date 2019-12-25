import graphene
import bcrypt
from bson.objectid import ObjectId
from ..database import UserModel
from mongoengine import DoesNotExist


class User:
    def __init__(self, email=None, user=None, id=None):
        if user != None:
            self._user = user
        elif id != None:
            if (ObjectId.is_valid(id)):
                self._user = UserModel.objects.get(id=ObjectId(id))
            else:
                raise DoesNotExist("ID not valid!")
        elif email != None:
            self._user = UserModel.objects.get(email=email)
        else:
            raise AttributeError("""
            Require one of email, user, id
        """)

    @classmethod
    def create(cls, email, name, password, role, image=None, introduction=None):
        password = bcrypt.hashpw(password, bcrypt.gensalt())
        user = UserModel(
            email=email,
            name=name,
            password=password,
            role=role,
            image=image,
            introduction=introduction
        )
        user.save()
        user.reload()
        return cls(user=user)

    @staticmethod
    def get_all():
        return list(UserModel.objects.all())

    def save(self):
        self._user.save()
        self._user.reload()

    def delete(self):
        self._user.delete()

    def get(self):
        return self._user

    def update_role(self, role):
        if role in ["Admin", "Doctor", "Nurse"]:
            self._user.role = role
            self.save()
        else:
            raise ValueError("Must be one of Admin, Doctor, Nurse!")

    def update_password(self, password):
        self._user.password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.save()

    def check_password(self, password):
        return bcrypt.checkpw(password, self._user.password)

    def update(self, user):
        self._user.update(**user)
        self.save()

    def get_id(self):
        return str(self._user['id'])

    def get_email(self):
        return self._user['email']

    def is_authenticated(self):
        return True if self.get_id() is not None else False

    def is_active(self):
        return True

    def is_anonymous(self):
        return not self.is_authenticated

    def get_urole(self):
        return self._user['role'] or "ANY"

    def get_name(self):
        return self._user['name']

    def get_password(self):
        return self._user['password']

    def get_image(self):
        return self._user['image']

    def get_introduction(self):
        return self._user['introduction']
