import pytest


def test_login_failed(user_client):
    res = user_client.post("/login", data={'{"email": "admin@gmail.com", "password": "asd" }': ''})
    assert res.status_code == 401


def test_login_None(user_client):
    res = user_client.post("/login", data={'{"email": "admin@gmail.com" }': ''})
    assert res.status_code == 401


def test_login(user_client):
    res = user_client.post(
        "/login", data={'{"email": "admin@gmail.com", "password": "admin" }': ''}
    )
    assert res.status_code == 200
    assert res.json['user']['email'] == "admin@gmail.com"


def test_logout(user_client):
    test_login(user_client)
    res = user_client.get("/logout")
    assert res.status_code == 200


def test_logout_before_login(user_client):
    res = user_client.get("/logout")
    assert res.status_code == 401


def test_check_failed(user_client):
    res = user_client.get("/check")
    assert res.status_code == 401


def test_check_failed(user_client):
    test_login(user_client)
    res = user_client.get("/check")
    assert res.status_code == 200
