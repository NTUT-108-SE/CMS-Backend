from ..fhir import InvoiceFHIR


class Invoice:

    fhir = InvoiceFHIR()

    def __init__(self, id=None, invoice=None):
        if invoice != None:
            self._invoice = invoice
        elif id != None:
            self._invoice, status_code = self.fhir.get_id(id)
            if status_code != 200:
                raise AttributeError("ID is invalid.")
        else:
            raise AttributeError("Invoice or ID must have one.")

    @classmethod
    def create(cls, date, patient_id, name, identifier, text):
        invoice = {
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
        }

        _invoice, status_code = cls.fhir.create(invoice)
        if status_code != 201:
            raise AttributeError("Invoice data is invalid.")

        return cls(invoice=_invoice)

    @classmethod
    def get_all(cls, offset=0, count=20):
        invoices, status_code = cls.fhir.get_all(offset, count)
        if status_code != 200:
            raise SystemError("FHIR Invoice API ERROR or FHIR SYSTEM Down")

        _invoices = []
        for entry in invoices.get('entry', []):
            _invoices.append(cls(invoice=entry['resource']))

        return {'total': invoices['total'], 'entry': _invoices, 'offset': offset, 'count': count}

    @classmethod
    def query_patient(cls, patient_id, offset=0, count=20):
        ivs, status_code = cls.fhir.query_patient(patient_id, offset, count)
        if status_code != 200:
            raise SystemError("FHIR INVOICE API ERROR or FHIR SYSTEM Down")

        _ivs = []
        for entry in ivs.get('entry', []):
            _ivs.append(cls(iv=entry['resource']))

        return {'total': ivs['total'], 'entry': _ivs, 'offset': offset, 'count': count}

    def get(self):
        return self._invoice

    @property
    def id(self):
        return self._invoice['id']

    @property
    def date(self):
        return self._invoice['date']

    @date.setter
    def date(self, new_date):
        self._invoice['date'] = new_date

    @property
    def patient_id(self):
        return self._invoice['subject']['reference'].split('/')[1]

    @property
    def name(self):
        return self._invoice['subject']['display']

    @name.setter
    def name(self, new_name):
        self._invoice['subject']['display'] = new_name

    @property
    def identifier(self):
        return self._invoice['subject']['identifier']['value']

    @identifier.setter
    def identifier(self, new_identifier):
        self._invoice['subject']['identifier']['value'] = new_identifier

    @property
    def text(self):
        return self._invoice['note'][0]['text']

    @text.setter
    def text(self, new_text):
        self._invoice['note'][0]['text'] = new_text
