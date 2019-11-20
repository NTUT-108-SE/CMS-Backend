import pytest


def test_login_failed(db_client):
    res = db_client.post("/login", data={'{"email": "test", "password": "test" }': ''})
    assert res.status_code == 401


def test_login_None(db_client):
    res = db_client.post("/login", data={'{"email": "test@gmail.com" }': ''})
    assert res.status_code == 401


def test_login(db_client):
    res = db_client.post("/login", data={'{"email": "test@gmail.com", "password": "test" }': ''})
    assert res.status_code == 200
    assert res.json['user']['email'] == "test@gmail.com"


def test_logout(db_client):
    test_login(db_client)
    res = db_client.get("/logout")
    assert res.status_code == 200


def test_logout_before_login(db_client):
    res = db_client.get("/logout")
    assert res.status_code == 401


def test_check_failed(db_client):
    res = db_client.get("/check")
    assert res.status_code == 401


def test_check_failed(db_client):
    test_login(db_client)
    res = db_client.get("/check")
    assert res.status_code == 200