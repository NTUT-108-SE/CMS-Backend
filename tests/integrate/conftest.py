import pytest
from app import create_app
from mongoengine import disconnect_all
from app.modules.domain.User import User


@pytest.fixture
def app():
    app = create_app('testing')

    yield app

    disconnect_all()


@pytest.fixture
def db_client(client):
    user1 = User.create(email="test@gmail.com", name="User1", password="test", role="Admin")
    user2 = User.create(email="test2@gmail.com", name="User2", password="test", role="Admin")
    yield client
    user1.delete()
    user2.delete()
