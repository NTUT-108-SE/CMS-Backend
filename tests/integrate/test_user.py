import pytest


def test_get_all_users(admin_client):
    res = admin_client.get("/user/all")
    assert res.status_code == 200
    assert res.json['ok'] == True


def test_get_user(admin_client):
    res = admin_client.get("/user/all")
    assert res.status_code == 200
    assert res.json['users'][0]['name'] == 'admin'

    res = admin_client.get("/user/" + res.json['users'][0]['id'])
    assert res.status_code == 200
    assert res.json['ok'] == True
    assert res.json['user']['name'] == 'admin'


def test_delete_user(admin_client):
    res = admin_client.get("/user/all")
    assert res.status_code == 200
    assert res.json['users'][1]['name'] == 'doctor'

    res2 = admin_client.delete("/user/" + res.json['users'][1]['id'])
    assert res2.json['ok'] == True

    res3 = admin_client.get("/user/" + res.json['users'][1]['id'])
    assert res3.json['ok'] == False


def test_create_user(admin_client):
    res = admin_client.post(
        "/user",
        data={
            '{"email": "test@gmail.com", "name": "test", "password": "test", "role": "Nurse" }': ''
        }
    )
    assert res.status_code == 200
    assert res.json['ok'] == True
    assert res.json['user']['name'] == 'test'