import requests


class FHIR:
    def get_all(self):
        # Todo GET
        # Get all data from FHIR
        pass

    def get_id(self, id):
        # Todo GET
        # Get this id data from FHIR
        pass

    def query_patient(self, patient_id):
        # Todo GET
        # Query data by patient_id
        pass

    def create(self, data):
        # Todo POST
        pass

    def delete(self, id):
        # Todo DELETE
        # Delete this id resource from FHIR
        pass

    def update(self, id, data):
        # Todo PUT
        # Update the data of this ID resource
        pass


class ConditionFHIR(FHIR):
    def __init__(self, uri="http://localhost:8080/hapi-fhir-jpaserver/fhir/"):
        self.uri = uri + "Condition"

    def get_all(self, offset=0, count=20):
        res = requests.get(self.uri + "?_getpagesoffset={}&_count={}".format(offset, count))
        return res.json(), res.status_code

    def get_id(self, id):
        res = requests.get(self.uri + "/{}".format(id))
        return res.json(), res.status_code

    def query_patient(self, patient_id, offset=0, count=20):
        res = requests.get(
            self.uri + "?patient={}&_getpagesoffset={}&_count={}".format(patient_id, offset, count)
        )
        return res.json(), res.status_code

    def create(self, data):
        res = requests.post(self.uri, json=data)
        return res.json(), res.status_code

    def delete(self, id):
        res = requests.delete(self.uri + "/{}".format(id))
        return res.json(), res.status_code

    def update(self, id, data):
        res = requests.put(self.uri + "/{}".format(id), json=data)
        return res.json(), res.status_code


class PatientFHIR(FHIR):
    def __init__(self, uri="http://localhost:8080/hapi-fhir-jpaserver/fhir/"):
        self.uri = uri + "Patient"

    def get_all(self, offset=0, count=20):
        res = requests.get(self.uri + "?_getpagesoffset={}&_count={}".format(offset, count))
        return res.json(), res.status_code

    def get_id(self, id):
        res = requests.get(self.uri + "/{}".format(id))
        return res.json(), res.status_code

    def query_patient(self, identifier):
        res = requests.get(self.uri + "?identifier={}".format(identifier))
        return res.json(), res.status_code

    def create(self, data):
        res = requests.post(self.uri, json=data)
        return res.json(), res.status_code

    def delete(self, id):
        res = requests.delete(self.uri + "/{}".format(id))
        return res.json(), res.status_code

    def update(self, id, data):
        res = requests.put(self.uri + "/{}".format(id), json=data)
        return res.json(), res.status_code


class InvoiceFHIR(FHIR):
    def __init__(self, uri="http://localhost:8080/hapi-fhir-jpaserver/fhir/"):
        self.uri = uri + "Invoice"

    def get_all(self, offset=0, count=20):
        res = requests.get(self.uri + "?_getpagesoffset={}&_count={}".format(offset, count))
        return res.json(), res.status_code

    def get_id(self, id):
        res = requests.get(self.uri + "/{}".format(id))
        return res.json(), res.status_code

    def query_patient(self, patient_id, offset=0, count=20):
        res = requests.get(
            self.uri + "?patient={}&_getpagesoffset={}&_count={}".format(patient_id, offset, count)
        )
        return res.json(), res.status_code

    def create(self, data):
        res = requests.post(self.uri, json=data)
        return res.json(), res.status_code


class MedicationFHIR(FHIR):
    def __init__(self, uri="http://localhost:8080/hapi-fhir-jpaserver/fhir/"):
        self.uri = uri + "MedicationKnowledge"

    def get_all(self, offset=0, count=20):
        res = requests.get(self.uri + "?_getpagesoffset={}&_count={}".format(offset, count))
        return res.json(), res.status_code

    def get_id(self, id):
        res = requests.get(self.uri + "/{}".format(id))
        return res.json(), res.status_code

    def create(self, data):
        res = requests.post(self.uri, json=data)
        return res.json(), res.status_code

    def delete(self, id):
        res = requests.delete(self.uri + "/{}".format(id))
        return res.json(), res.status_code

    def update(self, id, data):
        res = requests.put(self.uri + "/{}".format(id), json=data)
        return res.json(), res.status_code
