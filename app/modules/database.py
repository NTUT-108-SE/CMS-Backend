import re
from mongoengine import Document, EmailField, StringField, BooleanField, ListField, DateTimeField, DateField, IntField


class UserModel(Document):
    email = EmailField(unique=True, required=True)
    name = StringField(required=True, max_length=30)
    password = StringField(required=True)
    image = StringField()
    introduction = StringField()
    role = StringField(default="Nurse", regex=re.compile('(Nurse|Doctor|Admin)'))


class ManagementModel(Document):
    images = ListField(StringField(), required=True)  #require
    URLs = ListField(StringField(), required=True)  #require
    title = StringField(required=True)  #require
    time = StringField(required=True)  #require 當天結束看診時間
    description = StringField()
    our_services = StringField()
    doctor_description = StringField()
    clinic_address = StringField()


class AnnouncementModel(Document):
    title = StringField(required=True)  #require
    context = StringField(required=True)  #require
    author = StringField(required=True)  #require
    date = DateTimeField(required=True)  #require


class RegistrationModel(Document):
    identifier = StringField(required=True)
    name = StringField(required=True, max_length=30)
    birth_date = DateField(required=True)
    registration_date = DateField(required=True)
    order = IntField(required=True)
