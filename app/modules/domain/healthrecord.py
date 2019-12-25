from ..fhir import ConditionFHIR


class HealthRecord:

    fhir = ConditionFHIR()

    def __init__(self, id=None, hr=None):
        if hr != None:
            self._hr = hr
        elif id != None:
            self._hr, status_code = self.fhir.get_id(id)
            if status_code != 200:
                raise AttributeError("ID is invalid.")
        else:
            raise AttributeError()

    @classmethod
    def create(cls, patient_id, code, medication, date, identifier, name):
        health_record = {
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
        }

        hr, status_code = cls.fhir.create(health_record)
        if status_code != 201:
            raise AttributeError("health_record data is invalid.")

        return cls(hr=hr)

    def delete(self):
        self.fhir.delete(self.id)
        del self._hr

    @classmethod
    def get_all(cls, offset=0, count=20):
        hrs, status_code = cls.fhir.get_all(offset, count)
        if status_code != 200:
            raise SystemError("FHIR Condition API ERROR or FHIR SYSTEM Down")

        _hrs = []
        for entry in hrs.get('entry', []):
            _hrs.append(cls(hr=entry['resource']))

        return {'total': hrs['total'], 'entry': _hrs, 'offset': offset, 'count': count}

    @classmethod
    def query_patient(cls, patient_id, offset=0, count=20):
        hrs, status_code = cls.fhir.query_patient(patient_id, offset, count)
        if status_code != 200:
            raise SystemError("FHIR Condition API ERROR or FHIR SYSTEM Down")

        _hrs = []
        for entry in hrs.get('entry', []):
            _hrs.append(cls(hr=entry['resource']))

        return {'total': hrs['total'], 'entry': _hrs, 'offset': offset, 'count': count}

    def update(self, code, medication, identifier=None, name=None, date=None, patient_id=None):
        self.code = code
        self.medication = medication
        self.identifier = identifier
        self.name = name

        self._hr, status_code = self.fhir.update(self.id, self.get())
        if status_code != 200:
            raise AttributeError("health_record data is invalid.")

    def get(self):
        return self._hr

    @property
    def id(self):
        return self._hr['id']

    @property
    def patient_id(self):
        return self._hr['subject']['reference'].split('/')[1]

    @property
    def code(self):
        return self._hr['code']['text']

    @code.setter
    def code(self, new_code):
        self._hr['code']['text'] = new_code

    @property
    def medication(self):
        return self._hr['note'][0]['text']

    @medication.setter
    def medication(self, new_medication):
        self._hr['note'][0]['text'] = new_medication

    @property
    def date(self):
        return self._hr['recordedDate']

    @date.setter
    def date(self, new_date):
        self._hr['recordedDate'] = new_date

    @property
    def identifier(self):
        return self._hr['subject']['identifier']['value']

    @identifier.setter
    def identifier(self, new_identifier):
        self._hr['subject']['identifier']['value'] = new_identifier

    @property
    def name(self):
        return self._hr['subject']['display']

    @name.setter
    def name(self, new_name):
        self._hr['subject']['display'] = new_name
