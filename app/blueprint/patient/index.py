from . import patient
import json
from app.modules.login_manager import login_required
from flask import make_response, request
from flask.json import jsonify
from app.modules.graphql import graphql


@patient.route('all', methods=["GET"])
@login_required()
def get_all_patients():
    offset = request.args.get('offset', default=0, type=int)
    count = request.args.get('count', default=20, type=int)
    result = graphql.execute(
        '''
        query {
            patients(offset: %s, count: %s) {
                total
                    entry{
                        id
                        identifier
                        address
                        gender
                        family
                        given
                        phone
                        birthDate
                        maritalStatus
                }
                offset
                count
            }
        }
        ''' % (offset, count)
    ).data['patients']
    return make_response(jsonify({'ok': True, 'patients': result}), 200)


@patient.route('<patient_id>', methods=["GET"])
@login_required()
def get(patient_id):
    isId = True
    try:
        int(patient_id)
    except Exception:
        isId = False

    patient = None
    if isId:
        patient = graphql.execute(
            '''
            query {
                patient(id: %s) {
                    id
                    identifier
                    address
                    gender
                    family
                    given
                    phone
                    birthDate
                    maritalStatus
                }
            }
            ''' % patient_id
        ).data['patient']
    else:
        patient = graphql.execute(
            '''
            query {
                patient(identifier: "%s") {
                    id
                    identifier
                    address
                    gender
                    family
                    given
                    phone
                    birthDate
                    maritalStatus
                }
            }
            ''' % patient_id
        ).data['patient']

    return make_response(
        jsonify({
            'ok': True if patient != None else False,
            'patient': patient
        }), 200 if patient != None else 400
    )


@patient.route('<patient_id>', methods=["PUT"])
@login_required()
def change(patient_id):
    form = json.loads(list(request.form.keys())[0])
    identifier = form.get('identifier')
    address = form.get('address')
    gender = form.get('gender')
    family = form.get('family')
    given = form.get('given')
    phone = form.get('phone')
    birth_date = form.get('birthDate')
    marital_status = form.get('maritalStatus')
    if identifier is None or address is None or gender is None or family is None or given is None or marital_status is None or birth_date is None or phone is None:
        return make_response(jsonify({'ok': False, 'result': "Loss some patient data"}, 400))

    result = graphql.execute(
        '''
        mutation {
            mutatePatient(id: %s, patientData:{
                identifier: "%s",
                address: "%s",
                gender: "%s",
                family: "%s",
                given: "%s",
                phone: "%s",
                birthDate: "%s",
                maritalStatus: "%s"
            }) {
                ok
                patient{
                    id
                    identifier
                    address
                    gender
                    family
                    given
                    phone
                    birthDate
                    maritalStatus
                }
            }
        }
        ''' %
        (patient_id, identifier, address, gender, family, given, phone, birth_date, marital_status)
    ).data['mutatePatient']

    ok = result['ok']
    patient = result['patient']

    return make_response(jsonify({'ok': ok, 'patient': patient}), 200 if ok else 400)


@patient.route('<patient_id>', methods=["DELETE"])
@login_required()
def delete(patient_id):
    isId = True
    try:
        int(patient_id)
    except Exception:
        isId = False

    ok = False
    if isId:
        ok = graphql.execute(
            '''
            mutation {
                deletePatient(id: %s) {
                    ok
                }
        }''' % patient_id
        ).data['deletePatient']['ok']
    else:
        ok = graphql.execute(
            '''
            mutation {
                deletePatient(identifier: "%s") {
                    ok
                }
        }''' % patient_id
        ).data['deletePatient']['ok']

    return make_response(jsonify({'ok': ok}), 200 if ok else 400)


@patient.route('', methods=["POST"])
@login_required()
def create():
    form = json.loads(list(request.form.keys())[0])
    identifier = form.get('identifier')
    address = form.get('address')
    gender = form.get('gender')
    family = form.get('family')
    given = form.get('given')
    phone = form.get('phone')
    birth_date = form.get('birthDate')
    marital_status = form.get('maritalStatus')
    if identifier is None or address is None or gender is None or family is None or given is None or marital_status is None:
        return make_response(jsonify({'ok': False, 'result': "Loss some patient data"}, 400))

    check = graphql.execute(
        '''
            query {
                patient(identifier: "%s") {
                    id
                }
            }
            ''' % identifier
    ).data['patient']

    if check != None:
        return make_response(jsonify({'ok': False, 'result': "Already created"}), 400)

    result = graphql.execute(
        '''
        mutation {
            createPatient(patientData:{
                identifier: "%s",
                address: "%s",
                gender: "%s",
                family: "%s",
                given: "%s",
                phone: "%s",
                birthDate: "%s",
                maritalStatus: "%s"
            }) {
                ok
                patient{
                    id
                    identifier
                    address
                    gender
                    family
                    given
                    phone
                    birthDate
                    maritalStatus
                }
            }
        }
        ''' % (identifier, address, gender, family, given, phone, birth_date, marital_status)
    ).data['createPatient']

    ok = result['ok']
    patient = result['patient']
    return make_response(jsonify({'ok': ok, 'patient': patient}), 200 if ok else 400)
