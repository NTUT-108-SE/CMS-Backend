from ..fhir import invoiceFHIR


class Invoice:

    fhir = InvoiceFHIR()

    def __init__(self, id):
        if id != None:
            self._invoice, status_code = self.fhir.get_id(id)
            if status_code != 200:
                raise AttributeError("ID is invalid.")

    @classmethod
    def create(cls, date, reference, text):
        invoice = {
            "resourceType": "Invoice",
            "date": date,
            "subject": {
                "reference": "Patient/" + reference
            },
            "note": {
                "text": text
            }
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
    def reference(self)
        return self._invoice['subject']['reference']

    #getter & setter
