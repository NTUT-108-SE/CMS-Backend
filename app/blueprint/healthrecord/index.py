from flask import make_response, request
from datetime import datetime
from flask.json import jsonify
from app.modules.graphql import graphql
from app.modules.login_manager import login_required
from . import healthrecord
import json


@healthrecord.route('/<healthrecord_id>', methods=["GET"])
@login_required()
def get_healthrecord(healthrecord_id):
    hr = graphql.execute(
        '''
        query {
        healthRecord(id: %s) {
            id
            patientId
            code
            medication
            date
            identifier
            name
        }
    }
    ''' % healthrecord_id
    ).data['healthRecord']

    return make_response(
        jsonify({
            'ok': True if hr != None else False,
            'healthRecord': hr
        }), 200 if hr != None else 400
    )


@healthrecord.route('/all', methods=["GET"])
@login_required()
def get_all():
    offset = request.args.get('offset', default=0, type=int)
    count = request.args.get('count', default=20, type=int)
    patient_id = request.args.get('patientId', default=None, type=int)

    result = None
    if patient_id == None:
        result = graphql.execute(
            '''
        query {
            healthRecords(offset: %s, count: %s){
                total
                entry{
                    id
                    patientId
                    code
                    medication
                    date
                    identifier
                    name
                }
                offset
                count
            }
        }
        ''' % (offset, count)
        ).data['healthRecords']
    else:
        result = graphql.execute(
            '''
        query {
            healthRecords(offset: %s, count: %s, patientId: %s){
                total
                entry{
                    id
                    patientId
                    code
                    medication
                    date
                    identifier
                    name
                }
                offset
                count
            }
        }
        ''' % (offset, count, patient_id)
        ).data['healthRecords']
    return make_response(jsonify({'ok': True, 'healthrecords': result}), 200)


@healthrecord.route('', methods=["POST"])
@login_required()
def create():
    form = json.loads(list(request.form.keys())[0])
    patient_id = form.get('patientId')
    code = form.get('code')
    medication = form.get('medication')
    identifier = form.get('identifier')
    name = form.get('name')
    date = datetime.today().strftime('%Y-%m-%d')

    if patient_id is None or code is None or medication is None or identifier is None or name is None:
        return make_response(jsonify({'ok': False}), 400)

    result = graphql.execute(
        '''
    mutation {
        createHealthRecord(healthRecordData: {patientId: %s, code: "%s", medication: "%s", date: "%s", identifier: "%s", name: "%s"}) {
            ok
            healthRecord {
                id
                code
                medication
                patientId
                date
                identifier
                name
            }
        }
    }''' % (patient_id, code, medication, date, identifier, name)
    ).data['createHealthRecord']

    ok = result['ok']
    hr = result['healthRecord']

    return make_response(jsonify({'ok': ok, 'healthRecord': hr}), 200 if ok else 400)


@healthrecord.route('/<healthrecord_id>', methods=["PUT"])
@login_required()
def change(healthrecord_id):
    form = json.loads(list(request.form.keys())[0])
    code = form.get('code')
    medication = form.get('medication')
    identifier = form.get('identifier')
    name = form.get('name')

    if code is None or medication is None or identifier is None or name is None:
        return make_response(jsonify({'ok': False}), 400)

    result = graphql.execute(
        '''
    mutation {
        mutateHealthRecord(id: %s,healthRecordData: {code: "%s", medication: "%s", identifier: "%s", name: "%s"}) {
            ok
            healthRecord {
                id
                code
                medication
                patientId
                date
                identifier
                name
            }
        }
    }''' % (healthrecord_id, code, medication, identifier, name)
    ).data['mutateHealthRecord']

    ok = result['ok']
    hr = result['healthRecord']

    return make_response(jsonify({'ok': ok, 'healthRecord': hr}), 200 if ok else 400)


@healthrecord.route('/<healthrecord_id>', methods=["DELETE"])
@login_required()
def delete(healthrecord_id):
    ok = graphql.execute(
        '''
    mutation {
        deleteHealthRecord(id: %s) {
            ok
        }
    }''' % healthrecord_id
    ).data['deleteHealthRecord']['ok']
    return make_response(jsonify({'ok': ok}), 200 if ok else 400)
