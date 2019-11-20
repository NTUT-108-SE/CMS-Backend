import pytest
from app import create_app
from mongoengine import disconnect_all


@pytest.fixture
def app():
    app = create_app('testing')
    yield app
    disconnect_all()