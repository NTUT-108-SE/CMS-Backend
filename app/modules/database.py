import re
from mongoengine import Document, EmailField, StringField, URLField, BooleanField


class User(Document):
    email = EmailField(unique=True, required=True)
    name = StringField(required=True, max_length=30)
    password = StringField(required=True)
    image = URLField()
    introduction = StringField()
    role = StringField(default="Nurse", regex=re.compile('(Nurse|Doctor|Admin)'))
