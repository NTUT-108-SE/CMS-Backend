import pytest


def test_main(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json == {"success": True}


def test_logout(client):
    res = client.get("/logout")
    assert res.status_code == 401
