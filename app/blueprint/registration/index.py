import json
from datetime import datetime
from . import registration
from app.modules.graphql import graphql
from app.modules.login_manager import login_required
from flask import make_response, request
from flask.json import jsonify


@registration.route('<registration_id>', methods=["GET"])
@login_required()
def get(registration_id):
    registration = graphql.execute(
        '''
    query {
      registration(id: "%s") {
            name
            identifier
            birthDate
            registrationDate
            order
        }
    }
    ''' % registration_id
    ).data['registration']
    if registration == None:
        return make_response(jsonify({'ok': False}), 400)

    return make_response(jsonify({'ok': True, 'registration': registration}), 200)


@registration.route('identifier', methods=["GET"])
def get_identifier_registrations():
    identifier = request.args.get('identifier')

    registrations = graphql.execute(
        '''
    query {
      registrations(identifier: "%s") {
            name
            registrationDate
            order
        }
    }
    ''' % (identifier)
    ).data['registrations']

    return make_response(jsonify({'ok': True, 'registrations': registrations}), 200)


@registration.route('', methods=["GET"])
@login_required()
def get_registrations():
    identifier = request.args.get('identifier')
    date = request.args.get('date')

    registrations = graphql.execute(
        '''
    query {
      registrations(identifier: "%s", registrationDate: "%s") {
            id
            name
            identifier
            birthDate
            registrationDate
            order
        }
    }
    ''' % (identifier, date)
    ).data['registrations']

    return make_response(jsonify({'ok': True, 'registrations': registrations}), 200)


@registration.route('order', methods=["GET"])
def get_current_order():
    identifier = None
    date = datetime.today().strftime('%Y-%m-%d')

    registrations = graphql.execute(
        '''
    query {
      registrations(identifier:"%s", registrationDate: "%s") {
            id
            name
            identifier
            birthDate
            registrationDate
            order
        }
    }
    ''' % (identifier, date)
    ).data['registrations']
    if len(registrations) == 0:
        return make_response(jsonify({'ok': True, 'order': 0, 'total': 0}), 200)
    return make_response(
        jsonify({
            'ok': True,
            'order': registrations[0]['order'],
            'total': len(registrations)
        }), 200
    )


@registration.route('time', methods=["POST"])
@login_required()
def set_time():
    form = json.loads(list(request.form.keys())[0])
    time = form.get('time')

    if time is None:
        return make_response(jsonify({'ok': False}, 400))

    result = graphql.execute(
        '''
     mutation{
        mutateManagement(managementData:{
            time: "%s",
        }){
            ok
            management{
                title
                time
            }
        }
    }
    ''' % time
    ).data['mutateManagement']
    ok = result['ok']
    time = result['management']['time']

    return make_response(jsonify({'ok': True, 'time': time}), 200 if ok else 400)


@registration.route('<registration_id>', methods=["DELETE"])
@login_required()
def delete(registration_id):
    ok = graphql.execute(
        '''
        mutation {
            deleteRegistration(id: "%s") {
                ok
            }
        }
        ''' % registration_id
    ).data['deleteRegistration']['ok']
    return make_response(jsonify({'ok': ok}), 200 if ok else 400)


@registration.route('', methods=["POST"])
def create():
    form = json.loads(list(request.form.keys())[0])
    identifier = form.get('identifier')
    birth_date = form.get('birthDate')
    registration_date = form.get('registrationDate')
    patient_name = get_patient_name(identifier)

    if is_registration_end(registration_date):
        return make_response(
            jsonify({
                'ok': False,
                'message': "The registration time has passed"
            }), 400
        )

    if identifier == None or registration_date == None or birth_date == None or patient_name == None:
        return make_response(jsonify({'ok': False, 'message': 'Something is missing'}), 400)

    name = patient_name['family'] + patient_name['given']
    latest_order = get_latest_order(registration_date)
    order = latest_order + 1 if latest_order else 1

    result = graphql.execute(
        '''
        mutation {
            createRegistration(registrationData: {
                identifier:"%s"
                name: "%s"
                birthDate: "%s"
                registrationDate: "%s"
                order: "%d"
            }) {
                ok 
                registration {
                    id
                    identifier
                    name
                    birthDate
                    registrationDate
                    order
                }
            }
        }
        ''' % (identifier, name, birth_date, registration_date, order)
    ).data['createRegistration']

    ok = result['ok']
    registration = result['registration']

    return make_response(jsonify({'ok': ok, 'registration': registration}), 200 if ok else 400)


def get_patient_name(identifier):
    patient_name = graphql.execute(
        '''
        query {
            patient(identifier: "%s") {
                family
                given
            }
        }
        ''' % identifier
    ).data['patient']
    return patient_name


def get_latest_order(registration_date):
    latest_order = graphql.execute(
        '''
        query {
            latestOrder(registrationDate: "%s")
        }
        ''' % registration_date
    ).data['latestOrder']
    return latest_order


def get_registration_time():
    management = graphql.execute(
        '''
    query {
        management { 
            time
        }
    }
    '''
    ).data['management']
    return management['time']


def is_registration_end(registration_date):
    if registration_date != datetime.today().strftime("%Y-%m-%d"):
        return False

    current_hour = datetime.now().hour
    current_minute = datetime.now().minute

    try:
        registration_time = datetime.strptime(get_registration_time(), "%H:%M")
        registration_hour = registration_time.hour
        registration_minute = registration_time.minute
        if (current_hour > registration_hour):
            return True
        elif (current_hour == registration_hour and current_minute > registration_minute):
            return True
        return False
    except Exception:
        return True


@registration.route('next', methods=["GET"])
@login_required()
def next():
    registration_date = datetime.today().strftime('%Y-%m-%d')
    result = graphql.execute(
        '''
     mutation {
        nextRegistration(registrationDate: "%s") {
            ok
            registrations {
                id
                name
                order
                identifier
                birthDate
                registrationDate
            }
        }
    }

    ''' % registration_date
    ).data['nextRegistration']

    ok = result['ok']
    registrations = result['registrations']
    return make_response(jsonify({'ok': ok, 'registrations': registrations}), 200 if ok else 400)


@registration.route('skip', methods=["GET"])
@login_required()
def skip():
    registration_date = datetime.today().strftime('%Y-%m-%d')

    result = graphql.execute(
        '''
       mutation {
        skipRegistration(registrationDate: "%s") {
            ok
                registrations {
                    id
                name
                order
                identifier
                birthDate
                registrationDate    
            }    
        }
    }
    ''' % registration_date
    ).data['skipRegistration']

    ok = result['ok']
    registrations = result['registrations']
    return make_response(jsonify({'ok': ok, 'registrations': registrations}), 200 if ok else 400)
