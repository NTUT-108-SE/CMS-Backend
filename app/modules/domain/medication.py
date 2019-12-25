from ..fhir import MedicationFHIR


class Medication:

    fhir = MedicationFHIR()

    def __init__(self, id=None, medication=None):
        if medication != None:
            self._medication = medication
        elif id != None:
            self._medication, status_code = self.fhir.get_id(id)
            if status_code != 200:
                raise AttributeError("ID is invalid.")
        else:
            raise AttributeError()

    @classmethod
    def create(cls, name, synonym, ingredient, dosage, patient_characteristics, contraindication):
        medication = {
            "resourceType": "MedicationKnowledge",
            "code": {
                "coding": [{
                    "display": name
                }]
            },
            "synonym": [synonym],
            "ingredient": [{
                "strength": {
                    "numerator": {
                        "code": ingredient
                    }
                }
            }],
            "administrationGuidelines": [{
                "dosage": [{
                    "dosage": [{
                        "text": dosage
                    }]
                }],
                "patientCharacteristics": [{
                    "value": [patient_characteristics]
                }]
            }],
            "contraindication": [{
                "display": contraindication
            }]
        }
        _medication, status_code = cls.fhir.create(medication)

        if status_code != 201:
            raise AttributeError("medication data is invalid.")
        return cls(medication=_medication)

    def delete(self):
        self.fhir.delete(self.id)
        del self._medication

    @classmethod
    def get_all(cls, offset=0, count=20):

        medications, status_code = cls.fhir.get_all(offset, count)
        if status_code != 200:
            raise SystemError("FHIR Medication API ERROR or FHIR SYSTEM Down")

        _medications = []
        for entry in medications.get('entry', []):
            _medications.append(cls(medication=entry['resource']))

        return {
            'total': medications['total'],
            'entry': _medications,
            'offset': offset,
            'count': count
        }

    def update(self, name, synonym, ingredient, contraindication, dosage, patient_characteristics):
        self.name = name
        self.synonym = synonym
        self.ingredient = ingredient
        self.contraindication = contraindication
        self.dosage = dosage
        self.patient_characteristics = patient_characteristics
        self._medication, status_code = self.fhir.update(self.id, self.get())
        if status_code != 200:
            raise AttributeError("medications data is invalid.")

    def get(self):
        return self._medication

    @property
    def id(self):
        return self._medication['id']

    @property
    def name(self):
        return self._medication['code']['coding'][0]['display']

    @name.setter
    def name(self, new_name):
        self._medication['code']['coding'][0]['display'] = new_name

    @property
    def synonym(self):
        return self._medication['synonym'][0]

    @synonym.setter
    def synonym(self, new_synonym):
        self._medication['synonym'][0] = new_synonym

    @property
    def ingredient(self):
        return self._medication['ingredient'][0]['strength']['numerator']['code']

    @ingredient.setter
    def ingredient(self, new_ingredient):
        self._medication['ingredient'][0]['strength']['numerator']['code'] = new_ingredient

    @property
    def contraindication(self):
        return self._medication['contraindication'][0]['display']

    @contraindication.setter
    def contraindication(self, new_contraindication):
        self._medication['contraindication'][0]['display'] = new_contraindication

    @property
    def dosage(self):
        return self._medication['administrationGuidelines'][0]['dosage'][0]['dosage'][0]['text']

    @dosage.setter
    def dosage(self, new_dosage):
        self._medication['administrationGuidelines'][0]['dosage'][0]['dosage'][0]['text'
                                                                                 ] = new_dosage

    @property
    def patient_characteristics(self):
        return self._medication['administrationGuidelines'][0]['patientCharacteristics'][0]['value'
                                                                                           ][0]

    @patient_characteristics.setter
    def patient_characteristics(self, new_patient_characteristics):
        self._medication['administrationGuidelines'][0]['patientCharacteristics'][0]['value'][
            0] = new_patient_characteristics
