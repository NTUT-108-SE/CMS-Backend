from unittest.mock import patch
from app.modules.domain.patient import Patient


@patch('app.modules.domain.patient.Patient.fhir')
def test_init(mock_fhir):
    mock_fhir.get_id.return_value = ({}, 200)
    patient = Patient(id=1)
    mock_fhir.get_id.return_value = ({}, 404)
    try:
        patient = Patient(id=1)
        assert True == False
    except Exception as err:
        assert "ID is invalid." == str(err)

    mock_fhir.query_patient.return_value = ({'total': 1, 'entry': [{'resource': {}}]}, 200)
    patient = Patient(identifier="H123456789")
    mock_fhir.query_patient.return_value = ({}, 400)
    try:
        patient = Patient(identifier="H123456789")
        assert True == False
    except Exception as err:
        assert "Identifier is invalid." == str(err)

    patient = Patient(patient={})


@patch('app.modules.domain.patient.Patient.fhir')
def test_create(mock_fhir):
    identifier = "H123456789"
    family = "family"
    given = "given"
    phone = "123456789"
    gender = "male"
    birth_date = "2000-01-01"
    address = "address"
    marital_status = "未婚"
    mock_fhir.create.return_value = return_value = ({
        "resourceType": "Patient",
        "identifier": [{
            "value": identifier
        }],
        "name": [{
            "family": family,
            "given": [given]
        }],
        "telecom": [{
            "system": "phone",
            "value": phone
        }],
        "gender": gender,
        "birthDate": birth_date,
        "address": [{
            "text": address
        }],
        "maritalStatus": {
            "text": marital_status
        }
    }, 201)
    patient = Patient.create(
        identifier, family, given, phone, gender, birth_date, address, marital_status
    )
    assert patient.get() == return_value[0]

    mock_fhir.create.return_value = ({}, 400)
    try:
        patient = Patient.create(
            identifier, family, given, phone, gender, birth_date, address, marital_status
        )
        assert True == False
    except Exception as err:
        assert "patient data is invalid." == str(err)


@patch('app.modules.domain.patient.Patient.fhir')
def test_delete(mock_fhir):
    _patient = {"id": 0}
    patient = Patient(patient=_patient)
    patient.delete()
    assert hasattr(patient, '_patient') is False


@patch('app.modules.domain.patient.Patient.fhir')
def test_update(mock_fhir):
    mock_fhir.query_patient.return_value = return_value = ({
        'total': 1,
        'entry': [{
            'resource': {}
        }]
    }, 200)
    patient = Patient(
        patient={
            "id": 1,
            "resourceType": "Patient",
            "identifier": [{
                "value": "1"
            }],
            "name": [{
                "family": "1",
                "given": ["1"]
            }],
            "telecom": [{
                "system": "phone",
                "value": "1"
            }],
            "gender": "1",
            "birthDate": "1",
            "address": [{
                "text": "1"
            }],
            "maritalStatus": {
                "text": "1"
            }
        }
    )
    identifier = "H123456789"
    family = "family"
    given = "given"
    phone = "123456789"
    gender = "male"
    birth_date = "2000-01-01"
    address = "address"
    marital_status = "未婚"
    mock_fhir.update.return_value = return_value = ({
        "resourceType": "Patient",
        "identifier": [{
            "value": identifier
        }],
        "name": [{
            "family": family,
            "given": [given]
        }],
        "telecom": [{
            "system": "phone",
            "value": phone
        }],
        "gender": gender,
        "birthDate": birth_date,
        "address": [{
            "text": address
        }],
        "maritalStatus": {
            "text": marital_status
        }
    }, 200)
    patient.update(identifier, family, given, phone, gender, birth_date, address, marital_status)
    assert patient._patient == return_value[0]


@patch('app.modules.domain.patient.Patient.fhir')
def test_get(mock_fhir):
    identifier = "H123456789"
    family = "family"
    given = "given"
    phone = "123456789"
    gender = "male"
    birth_date = "2000-01-01"
    address = "address"
    marital_status = "未婚"
    return_value = {
        "resourceType": "Patient",
        "id": 1,
        "identifier": [{
            "value": identifier
        }],
        "name": [{
            "family": family,
            "given": [given]
        }],
        "telecom": [{
            "system": "phone",
            "value": phone
        }],
        "gender": gender,
        "birthDate": birth_date,
        "address": [{
            "text": address
        }],
        "maritalStatus": {
            "text": marital_status
        }
    }

    patient = Patient(patient=return_value)

    assert identifier == patient.identifier
    assert family == patient.family
    assert given == patient.given
    assert phone == patient.phone
    assert gender == patient.gender
    assert birth_date == patient.birth_date
    assert address == patient.address
    assert marital_status == patient.marital_status
    assert patient.get() == return_value
