from . import invoice
import json
from app.modules.login_manager import login_required
from flask import make_response, request
from flask.json import jsonify
from app.modules.graphql import graphql


@invoice.route('all', methods=["GET"])
@login_required()
def get_all_invoices():
    offset = request.args.get('offset', default=0, type=int)
    count = request.args.get('count', default=20, type=int)
    result = graphql.execute(
        '''
        query{
            invoices(offset: %s, count: %s){
                total,
                entry {
                    id
                    date
                    patientId
                    name
                    identifier
                    text
                },
                offset,
                count
            }
        }
        ''' % (offset, count)
    ).data['invoices']

    return make_response(jsonify({'ok': True, 'invoices': result}), 200)


@invoice.route('', methods=["GET"])
@login_required()
def get_patient_invoices():
    offset = request.args.get('offset', default=0, type=int)
    count = request.args.get('count', default=20, type=int)
    patient_id = request.args.get('patientId', None)
    result = graphql.execute(
        '''
        query{
            invoices(offset: %s, count: %s){
                total,
                entry {
                    id
                    date
                    patientId
                    name
                    identifier
                    text
                },
                offset,
                count
            }
        }
        ''' % (offset, count)
    ).data['invoices']

    return make_response(jsonify({'ok': True, 'invoices': result}), 200)


@invoice.route('<invoice_id>', methods=["GET"])
@login_required()
def get(invoice_id):
    isId = True
    try:
        int(invoice_id)
    except Exception:
        isId = False

    invoice = None
    if isId:
        invoice = graphql.execute(
            '''
            query {
                invoice(id: %s) {
                    id
                    date
                    patientId
                    name
                    identifier
                    text
                }
            }
            ''' % invoice_id
        ).data['invoice']

    return make_response(
        jsonify({
            'ok': True if invoice != None else False,
            'invoice': invoice
        }), 200 if invoice != None else 400
    )


@invoice.route('', methods=["POST"])
@login_required()
def create():
    form = json.loads(list(request.form.keys())[0])
    date = form.get('date')
    patient_id = form.get('patientId')
    name = form.get('name')
    identifier = form.get('identifier')
    text = form.get('text')

    if date is None or patient_id is None or name is None or identifier is None or text is None:
        return make_response(jsonify({'ok': False, 'result': "Loss some invoice data"}, 400))

    result = graphql.execute(
        '''
        mutation{
            createInvoice(invoiceData:{
                date: "%s",
                patientId: %s,
                name: "%s",
                identifier: "%s",
                text: "%s"
            }){
                ok
                invoice{
                    id
                    date
                    patientId
                    name
                    identifier
                    text
                }
            }
        }
        ''' % (date, patient_id, name, identifier, text)
    ).data['createInvoice']

    ok = result['ok']

    return make_response(jsonify({'ok': ok, 'invoice': result['invoice']}), 200 if ok else 400)
