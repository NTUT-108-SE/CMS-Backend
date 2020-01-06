import pytest
from app import create_app
from mongoengine import disconnect_all
from app.modules.domain.user import User
from app.modules.domain.announcement import Announcement


@pytest.fixture
def app():
    app = create_app('testing')
    yield app
    disconnect_all()


@pytest.fixture
def user_client(client):
    admin = User.create(
        email="admin@gmail.com",
        name="admin",
        password="admin",
        role="Admin",
        image="",
        introduction=""
    )
    doctor = User.create(
        email="doctor@gmail.com",
        name="doctor",
        password="doctor",
        role="Doctor",
        image="",
        introduction=""
    )
    nurse = User.create(
        email="nurse@gmail.com",
        name="nurse",
        password="nurse",
        role="Nurse",
        image="",
        introduction=""
    )
    yield client
    admin.delete()
    doctor.delete()
    nurse.delete()


@pytest.fixture
def admin_client(user_client):
    res = user_client.post(
        "/login", data={'{"email": "admin@gmail.com", "password": "admin" }': ''}
    )
    assert res.status_code == 200

    yield user_client

    res = user_client.get("/logout")
    assert res.status_code == 200


@pytest.fixture
def management_client(admin_client):
    ann1 = Announcement.create("test title", "test context", "admin", "2010-10-10")
    ann2 = Announcement.create("test title2", "test context2", "admin", "2010-10-10")

    yield admin_client

    ann1.delete()
    ann2.delete()
