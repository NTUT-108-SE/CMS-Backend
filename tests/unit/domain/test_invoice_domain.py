from unittest.mock import patch
from app.modules.domain.invoice import Invoice


@patch('app.modules.domain.invoice.Invoice.fhir')
def test_create(mock_fhir):
    date = "1987-08-07"
    patient_id = "88"
    name = "My name is victor reznov"
    identifier = "A123456789"
    text = "This is my revenge"
    mock_fhir.create.return_value = return_value = ({
        "resourceType": "Invoice",
        "date": date,
        "subject": {
            "reference": "Patient/{}".format(patient_id),
            "display": name,
            "identifier": {
                'value': identifier
            }
        },
        "note": [{
            "text": text
        }]
    }, 201)
    invoice = Invoice.create(date, patient_id, name, identifier, text)
    assert invoice.get() == return_value[0]
    assert invoice.date == date
    assert invoice.patient_id == patient_id
    assert invoice.name == name
    assert invoice.identifier == identifier
    assert invoice.text == text

    mock_fhir.create.return_value = ({}, 400)
    try:
        invoice = Invoice.create(date, patient_id, name, identifier, text)
        assert True == False
    except Exception as err:
        assert "Invoice data is invalid." == str(err)


@patch('app.modules.domain.invoice.Invoice.fhir')
def test_get(mock_fhir):
    date = "1987-08-07"
    patient_id = "88"
    name = "My name is victor reznov"
    identifier = "A123456789"
    text = "This is my revenge"
    return_value = {
        "resourceType": "Invoice",
        "id": "88",
        "date": date,
        "subject": {
            "reference": "Patient/{}".format(patient_id),
            "display": name,
            "identifier": {
                'value': identifier
            }
        },
        "note": [{
            "text": text
        }]
    }

    invoice = Invoice(invoice=return_value)

    assert invoice.get() == return_value
    assert invoice.date == date
    assert invoice.patient_id == patient_id
    assert invoice.name == name
    assert invoice.identifier == identifier
    assert invoice.text == text
