from unittest.mock import patch
from app.modules.domain.healthrecord import HealthRecord


@patch('app.modules.domain.healthrecord.HealthRecord.fhir')
def test_init(mock_fhir):
    mock_fhir.get_id.return_value = ({}, 200)
    hr = HealthRecord(id=1)
    mock_fhir.get_id.return_value = ({}, 404)
    try:
        hr = HealthRecord(id=1)
        assert True == False
    except Exception as err:
        assert "ID is invalid." == str(err)

    mock_fhir.query_patient.return_value = ({'total': 1, 'entry': [{'resource': {}}]}, 200)
    hr = HealthRecord.query_patient(patient_id=1)
    mock_fhir.query_patient.return_value = ({}, 400)
    try:
        hr = HealthRecord.query_patient(patient_id=1)
        assert True == False
    except Exception as err:
        assert "FHIR Condition API ERROR or FHIR SYSTEM Down" == str(err)

    hr = HealthRecord(hr={})


@patch('app.modules.domain.healthrecord.HealthRecord.fhir')
def test_create(mock_fhir):
    date = "2000-10-10"
    patient_id = 1
    name = "test"
    identifier = "H123456789"
    code = "1234"
    medication = "12345"
    mock_fhir.create.return_value = return_value = ({
        "resourceType": "Condition",
        "recordedDate": date,
        "subject": {
            "reference": "Patient/{}".format(patient_id),
            "display": name,
            "identifier": {
                'value': identifier
            },
        },
        "code": {
            "text": code
        },
        "note": {
            "text": medication
        }
    }, 201)
    hr = HealthRecord.create(patient_id, code, medication, date, identifier, name)
    assert hr.get() == return_value[0]

    mock_fhir.create.return_value = ({}, 400)
    try:
        hr = HealthRecord.create(patient_id, code, medication, date, identifier, name)
        assert True == False
    except Exception as err:
        assert "health_record data is invalid." == str(err)


@patch('app.modules.domain.healthrecord.HealthRecord.fhir')
def test_delete(mock_fhir):
    _hr = {"id": 0}
    hr = HealthRecord(hr=_hr)
    hr.delete()
    mock_fhir.delete.assert_called_once()


@patch('app.modules.domain.healthrecord.HealthRecord.fhir')
def test_update(mock_fhir):
    _hr = {
        "resourceType": "Condition",
        "id": "96",
        "meta": {
            "versionId": "1",
            "lastUpdated": "2019-12-18T15:29:03.000+00:00"
        },
        "code": {
            "text": "ghhgofh"
        },
        "subject": {
            "reference": "Patient/56",
            "identifier": {
                "value": "H123456789"
            },
            "display": "姓氏名字"
        },
        "recordedDate": "2019-12-18",
        "note": [{
            "text": "ghhggfh"
        }]
    }

    hr = HealthRecord(hr=_hr)

    mock_fhir.update.return_value = (_hr, 200)
    hr.update("1", "2", "3", "4")
    mock_fhir.update.return_value = (_hr, 400)
    try:
        hr.update("1", "2", "3", "4")
        assert True == False
    except Exception as err:
        assert "health_record data is invalid." == str(err)


@patch('app.modules.domain.healthrecord.HealthRecord.fhir')
def test_get(mock_fhir):
    _hr = {
        "resourceType": "Condition",
        "id": "96",
        "meta": {
            "versionId": "1",
            "lastUpdated": "2019-12-18T15:29:03.000+00:00"
        },
        "code": {
            "text": "ghhgofh"
        },
        "subject": {
            "reference": "Patient/56",
            "identifier": {
                "value": "H123456789"
            },
            "display": "姓氏名字"
        },
        "recordedDate": "2019-12-18",
        "note": [{
            "text": "ghhggfh"
        }]
    }

    hr = HealthRecord(hr=_hr)

    assert hr.get() == _hr
    assert hr.id == "96"
    assert hr.code == "ghhgofh"
    assert hr.medication == "ghhggfh"
    assert hr.date == "2019-12-18"
    assert hr.identifier == "H123456789"
    assert hr.name == "姓氏名字"


@patch('app.modules.domain.healthrecord.HealthRecord.fhir')
def test_get_all(mock_fhir):
    _hrs = {
        "total":
            1,
        "count":
            20,
        "offset":
            0,
        "entry": [{
            "resource": {
                "resourceType": "Condition",
                "id": "96",
                "meta": {
                    "versionId": "1",
                    "lastUpdated": "2019-12-18T15:29:03.000+00:00"
                },
                "code": {
                    "text": "ghhgofh"
                },
                "subject": {
                    "reference": "Patient/56",
                    "identifier": {
                        "value": "H123456789"
                    },
                    "display": "姓氏名字"
                },
                "recordedDate": "2019-12-18",
                "note": [{
                    "text": "ghhggfh"
                }]
            }
        }]
    }

    mock_fhir.get_all.return_value = return_value = (_hrs, 200)
    hrs = HealthRecord.get_all()
    mock_fhir.get_all.assert_called_once()

    mock_fhir.get_all.return_value = return_value = ({}, 400)

    try:
        hrs = HealthRecord.get_all()
        assert True == False
    except Exception as err:
        assert "FHIR Condition API ERROR or FHIR SYSTEM Down" == str(err)
