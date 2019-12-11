import pytest
from mongoengine import connect, disconnect
from app.modules.domain.User import User


@pytest.fixture
def db():
    connect('mongoenginetest', host='mongomock://localhost')
    yield
    disconnect()


@pytest.fixture
def db_user(db):
    user1 = User.create(email="test@gmail.com", name="User1", password="test", role="Admin")
    user2 = User.create(email="test2@gmail.com", name="User2", password="test", role="Admin")
    yield
    user1.delete()
    user2.delete()
