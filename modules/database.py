from mongoengine import Document, EmailField, StringField, URLField


class User(Document):
    email = EmailField(unique=True, required=True)
    name = StringField(required=True, max_length=30)
    password = StringField(required=True)
    image = URLField()
    introduction = StringField()