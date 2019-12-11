import graphene
import bcrypt
from bson.objectid import ObjectId
from ..database import UserModel
from graphene_mongo import MongoengineObjectType
from mongoengine import DoesNotExist


class User(MongoengineObjectType):
    class Meta:
        model = UserModel

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

    def get_json(self):
        return self._user.to_json()

    def save_hash_pass(self, password):
        self._user.password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.save()

    def check_password(self, password):
        return bcrypt.checkpw(password, self._user.password)

    def update(self, user):
        self._user.update(user)
        self.save()

    def get_id(self):
        return str(self._user['id'])

    def get_email(self):
        return self._user['email']

    def is_authenticated(self):
        return True if self._user.get('id') is not None else False

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