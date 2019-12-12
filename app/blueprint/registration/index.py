from . import registration
import json
from app.modules.login_manager import login_required
from flask import make_response, request
from flask.json import jsonify


@registration.route('all', methods=["GET"])
@login_required()
def get_all_registrations():
    registrations = [{
        "onlineRegistrationNum": "0",
        "patientID": "A000000000",
        "name": "前端測試帳號",
        "registrationDate": "2019-10-20",
        "birthDate": "2019-10-20"
    }, {
        "onlineRegistrationNum": "1",
        "patientID": "A000000001",
        "name": "前端測試帳號",
        "registrationDate": "2019-10-20",
        "birthDate": "2019-10-20"
    }, {
        "onlineRegistrationNum": "2",
        "patientID": "A000000002",
        "name": "前端測試帳號",
        "registrationDate": "2019-10-20",
        "birthDate": "2019-10-21"
    }]
    return make_response(jsonify({'ok': True, 'registrations': registrations}), 200)


@registration.route('<registration_id>', methods=["GET"])
@login_required()
def get(registration_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': registration_id}), 200)


@registration.route('', methods=["GET"])
@login_required()
def get_patient_registrations():
    #Todo
    patient_id = request.args.get('patientID', None)
    return make_response(jsonify({'ok': True, 'result': patient_id}), 200)


@registration.route('time', methods=["POST"])
@login_required()
def set_time():
    #Todo
    return make_response(jsonify({'ok': True, 'result': 'set time'}), 200)


@registration.route('datetime/<datetime>', methods=["GET"])
@login_required()
def get_datetime(datetime):
    #Todo
    return make_response(jsonify({'ok': True, 'result': datetime}), 200)


@registration.route('<registration_id>', methods=["PUT"])
@login_required()
def change(registration_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': registration_id + ' changed'}), 200)


@registration.route('<registration_id>', methods=["DELETE"])
@login_required()
def delete(registration_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': registration_id + ' deleted'}), 200)


@registration.route('', methods=["POST"])
@login_required()
def create():
    #Todo
    return make_response(jsonify({'ok': True, 'result': 'created'}), 200)


@registration.route('next', methods=["POST"])
@login_required()
def next():
    #Todo
    return make_response(jsonify({'ok': True, 'result': 'next'}), 200)


@registration.route('skip', methods=["POST"])
@login_required()
def skip():
    #Todo
    return make_response(jsonify({'ok': True, 'result': 'skip'}), 200)
