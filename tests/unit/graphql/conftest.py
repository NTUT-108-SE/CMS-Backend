import pytest
from mongoengine import connect, disconnect
from app.modules import database


@pytest.fixture
def db():
    connect('mongoenginetest', host='mongomock://localhost')
    yield database
    disconnect()


@pytest.fixture
def db_user(db):
    user1 = db.User("test@gmail.com", name="User1", password="test").save()
    user2 = db.User("test2@gmail.com", name="User2", password="test").save()
    yield db
    user1.delete()
    user2.delete()
