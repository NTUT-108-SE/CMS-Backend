def test_get(management_client):
    info = management_client.get('/management')
    assert True == info.json['ok']
    assert "Default_title" == info.json['management']['title']


def test_change(management_client):
    test_data = {
        '''{
        "images": [
            "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
            "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
            "https://cdn.vuetifyjs.com/images/carousel/bird.jpg",
            "https://cdn.vuetifyjs.com/images/carousel/planet.jpg"
        ],
        "URLs": [
            "https://google.com", "https://google.com", "https://google.com", "https://google.com"
        ],
        "title": "Default_title1",
        "time": "19:01",
        "description": "Default_description",
        "ourServices": "Default_our_services",
        "doctorDescription": "Default_doctor_description",
        "clinicAddress": "Default_clinic_address"
    }''':
            ''
    }

    res = management_client.put('/management/information', data=test_data)
    assert res.status_code == 200
    assert res.json['ok'] == True
    assert res.json['management']['title'] == "Default_title1"


def test_get_announcements(management_client):
    res = management_client.get('/management/announcements')
    assert res.status_code == 200
    assert res.json['ok'] == True
    assert res.json['announcements']['total'] == 2
    assert res.json['announcements']['entry'][0]['title'] == 'test title2'


def test_get_announcement(management_client):
    res = management_client.get('/management/announcements')
    assert res.status_code == 200
    assert res.json['ok'] == True
    assert res.json['announcements']['total'] == 2
    assert res.json['announcements']['entry'][0]['title'] == 'test title2'

    res2 = management_client.get(
        '/management/announcement/{}'.format(res.json['announcements']['entry'][0]['id'])
    )
    assert res2.json['ok'] == True
    assert res2.json['announcement']['title'] == 'test title2'


def test_create_announcement(management_client):
    test_data = {
        '''{
        "title": "test title3",
        "context": "test context3",
        "author": "author",
        "date": "2010-10-10"
    }''':
            ''
    }

    res = management_client.post('/management/announcement', data=test_data)
    assert res.status_code == 200
    assert res.json['ok'] == True
    assert res.json['announcement']['title'] == "test title3"


def test_change_announcement(management_client):
    test_data = {
        '''{
        "title": "test title3",
        "context": "test context3",
        "author": "author",
        "date": "2010-10-10"
    }''':
            ''
    }

    res = management_client.post('/management/announcement', data=test_data)
    assert res.status_code == 200
    assert res.json['ok'] == True
    assert res.json['announcement']['title'] == "test title3"
    test_data = {
        '''{
        "title": "test title4",
        "context": "test context4",
        "author": "author",
        "date": "2010-10-10"
    }''':
            ''
    }
    res2 = management_client.put(
        '/management/announcement/{}'.format(res.json['announcement']['id']), data=test_data
    )
    assert res2.status_code == 200
    assert res2.json['ok'] == True
    assert res2.json['announcement']['title'] == "test title4"


def test_delete(management_client):
    test_data = {
        '''{
        "title": "test title3",
        "context": "test context3",
        "author": "author",
        "date": "2010-10-10"
    }''':
            ''
    }

    res = management_client.post('/management/announcement', data=test_data)
    assert res.status_code == 200
    assert res.json['ok'] == True
    assert res.json['announcement']['title'] == "test title3"

    res2 = management_client.delete(
        '/management/announcement/{}'.format(res.json['announcement']['id'])
    )
    assert res2.status_code == 200
    assert res2.json['ok'] == True