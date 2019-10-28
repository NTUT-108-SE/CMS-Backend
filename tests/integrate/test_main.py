import pytest


async def test_main(client):
    res = client.get("/")
    assert res.status_code == 200
