from ..fhir import PatientFHIR


class Patient:

    fhir = PatientFHIR()

    def __init__(self, id=None, patient=None, identifier=None):
        if patient != None:
            self._patient = patient
        elif id != None:
            self._patient, status_code = self.fhir.get_id(id)
            if status_code != 200:
                raise AttributeError("ID is invalid.")
        elif identifier != None:
            _patient, status_code = self.fhir.query_patient(identifier)
            if status_code != 200 or _patient['total'] == 0:
                raise AttributeError("Identifier is invalid.")
            self._patient = _patient['entry'][0]['resource']
        else:
            raise AttributeError()

    @classmethod
    def create(cls, identifier, family, given, phone, gender, birth_date, address, marital_status):
        patient = {
            "resourceType": "Patient",
            "identifier": [{
                "value": identifier  # 身分證 required type:string
            }],
            "name": {
                "family": family,  # required type:string
                "given": given  # required type:string
            },
            "telecom": [{
                "system": "phone",  # type:code
                "value": phone  # required type:string limit:20
            }],
            "gender": gender,  # required type:code |male | female | other | unknown|
            "birthDate": birth_date,  #required type:date format: YYYY-MM-DD
            "address": {
                "text": address  # required type:string 
            },
            "maritalStatus": {
                "text": marital_status  #required 	未婚|已婚|離婚|喪偶|不願提供
            }
        }

        _patient, status_code = cls.fhir.create(patient)
        if status_code != 201:
            raise AttributeError("patient data is invalid.")

        return cls(patient=_patient)

    def delete(self):
        self.fhir.delete(self.id)
        del self._patient

    @classmethod
    def get_all(cls, offset=0, count=20):
        patients, status_code = cls.fhir.get_all(offset, count)
        if status_code != 200:
            raise SystemError("FHIR Patient API ERROR or FHIR SYSTEM Down")

        _patients = []
        for entry in patients.get('entry', []):
            _patients.append(cls(patient=entry['resource']))

        return {'total': patients['total'], 'entry': _patients, 'offset': offset, 'count': count}

    def update(self, identifier, family, given, phone, gender, birth_date, address, marital_status):
        self.identifier = identifier
        self.family = family
        self.given = given
        self.phone = phone
        self.gender = gender
        self.birth_date = birth_date
        self.address = address
        self.marital_status = marital_status

        self._patient, status_code = self.fhir.update(self.id, self.get())
        if status_code != 200:
            raise AttributeError("patient data is invalid.")

    def get(self):
        return self._patient

    @property
    def id(self):
        return self._patient['id']

    @property
    def identifier(self):
        return self._patient['identifier'][0]['value']

    @identifier.setter
    def identifier(self, new_identifier):
        self._patient['identifier'][0]['value'] = new_identifier

    @property
    def family(self):
        return self._patient['name'][0]['family']

    @family.setter
    def family(self, new_family):
        self._patient['name'][0]['family'] = new_family

    @property
    def given(self):
        return self._patient['name'][0]['given'][0]

    @given.setter
    def given(self, new_given):
        self._patient['name'][0]['given'][0] = new_given

    @property
    def phone(self):
        return self._patient['telecom'][0]['value']

    @phone.setter
    def phone(self, new_phone):
        self._patient['telecom'][0]['value'] = new_phone

    @property
    def gender(self):
        return self._patient['gender']

    @gender.setter
    def gender(self, new_gender):
        self._patient['gender'] = new_gender

    @property
    def birth_date(self):
        return self._patient['birthDate']

    @birth_date.setter
    def birth_date(self, new_birth_date):
        self._patient['birthDate'] = new_birth_date

    @property
    def address(self):
        return self._patient['address'][0]['text']

    @address.setter
    def address(self, new_address):
        self._patient['address'][0]['text'] = new_address

    @property
    def marital_status(self):
        return self._patient['maritalStatus']['text']

    @marital_status.setter
    def marital_status(self, new_marital_status):
        self._patient['maritalStatus']['text'] = new_marital_status
