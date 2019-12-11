from . import patient
import json
from app.modules.login_manager import login_required
from app.modules.schema import graphql
from flask_login import login_user, current_user
from flask import make_response, request
from flask.json import jsonify


@patient.route('all', methods=["GET"])
@login_required()
def get_all_patients():
    patients = [
        {
            'patientNum': '1',
            'patientID': "AXXXXXXXXX",
            'name': "前端測試帳號",
            'gender': "男",
            'birthDate': "2010-05-03",
            'createTime': "2019-10-20",
            'editTime': "2019-10-20"
        },
        {
            'patientNum': "1",
            'patientID': "DXXXXXXXXX",
            'name': "前端測試帳號",
            'gender': "女",
            'birthDate': "2010-05-03",
            'createTime': "2019-10-20",
            'editTime': "2019-10-20"
        }
    ]
    return make_response(jsonify({'ok': True, 'patients': patients}), 200)


@patient.route('<patient_id>', methods=["GET"])
@login_required()
def get(patient_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': patient_id}), 200)


@patient.route('<patient_id>', methods=["PUT"])
@login_required()
def change(patient_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': patient_id + ' changed'}), 200)

@patient.route('<patient_id>', methods=["DELETE"])
@login_required()
def delete(patient_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': patient_id + ' deleted'}), 200)

@patient.route('', methods=["POST"])
@login_required()
def create():
    #Todo
    return make_response(jsonify({'ok': True, 'result': 'created'}), 200)


