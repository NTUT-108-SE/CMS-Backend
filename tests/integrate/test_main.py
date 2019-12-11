import pytest


def test_main(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json == {"ok": True}


def test_error_page(client):
    res = client.get("/not-found-page")
    assert res.status_code == 404
    assert res.json == {"error": "Page not found!"}
