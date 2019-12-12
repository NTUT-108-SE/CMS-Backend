from . import medication
import json
from app.modules.login_manager import login_required
from app.modules.schema import graphql
from flask_login import login_user, current_user
from flask import make_response, request
from flask.json import jsonify


@medication.route('all', methods=["GET"])
@login_required()
def get_all_medications():
    medications = [
      {
        'pillNum': "0",
        'pillScientificName': "acetaminophen",
        'pillName': "普拿疼"
      },
      {
        'pillNum': "1",
        'pillScientificName': "aspirin",
        'pillName': "阿斯匹林"
      }
    ]
    return make_response(jsonify({'ok': True, 'medications': medications}), 200)


@medication.route('', methods=["GET"])
@login_required()
def get_patient_medications():
    patient_id = request.args.get('patientID', None)
    #Todo
    return make_response(jsonify({'ok': True, 'result': patient_id}), 200)

@medication.route('<medication_id>', methods=["GET"])
@login_required()
def get(medication_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': medication_id}), 200)

@medication.route('<medication_id>', methods=["PUT"])
@login_required()
def change(medication_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': medication_id + ' changed'}), 200)

@medication.route('<medication_id>', methods=["DELETE"])
@login_required()
def delete(medication_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': medication_id + ' deleted'}), 200)

@medication.route('', methods=["POST"])
@login_required()
def create():
    #Todo
    return make_response(jsonify({'ok': True, 'result': 'created'}), 200)
