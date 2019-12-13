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


def test_update_role(admin_client):
    res = admin_client.get("/user/all")
    assert res.json['ok'] == True
    assert res.json['users'][1]['name'] == 'doctor'

    res1 = admin_client.post("/user/" + res.json['users'][1]['id'], data={'{"role": "Admin"}': ''})
    assert res1.json['ok'] == True

    res2 = admin_client.get("/user/all")
    assert res2.json['users'][1]['name'] == 'doctor'
    assert res2.json['users'][1]['role'] == 'Admin'

    res1 = admin_client.post(
        "/user/" + res.json['users'][1]['id'], data={'{"role": "awiefwa"}': ''}
    )
    assert res1.json['ok'] == False


def test_change_user(admin_client):
    res = admin_client.put(
        "/user", data={'{"name": "test", "image":"test_image","introduction": "test_intro"}': ''}
    )
    assert res.json['ok'] == True
    assert res.json['user']['name'] == 'test'
    assert res.json['user']['image'] == 'test_image'
    assert res.json['user']['introduction'] == 'test_intro'


def test_change_password(admin_client):
    res = admin_client.post("/user/change_password", data={'{"password1": ""}': ''})
    assert res.json['ok'] == False

    res = admin_client.post(
        "/user/change_password", data={'{"old_password": "admin", "password": "test"}': ''}
    )
    assert res.json['ok'] == True

    res = admin_client.post(
        "/login", data={'{"email": "admin@gmail.com", "password": "test" }': ''}
    )
    assert res.json['ok'] == True
