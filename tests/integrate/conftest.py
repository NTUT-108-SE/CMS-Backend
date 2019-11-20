import pytest
from app import create_app
from mongoengine import disconnect_all
from app.modules import database


@pytest.fixture
def app():
    app = create_app('testing')

    yield app

    disconnect_all()


@pytest.fixture
def db_client(client):
    user1 = database.User("test@gmail.com", name="User1", password="test").save()
    user2 = database.User("test2@gmail.com", name="User2", password="test").save()
    yield client
    user1.delete()
    user2.delete()
