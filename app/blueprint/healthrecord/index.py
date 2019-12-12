from flask import make_response
from flask.json import jsonify
from app.modules.login_manager import login_required
from . import healthrecord


@healthrecord.route('/<healthrecord_id>', methods=["GET"])
@login_required()
def get_healthrecord(healthrecord_id):
    result = {
        'id': 1,
        'patient_id': healthrecord_id,
        'note': 'note test',
        'medication': 'medication test',
        'date': '2020-01-01'
    }

    return make_response(jsonify({'ok': True, 'healthrecord': result}), 200)


@healthrecord.route('/all', methods=["GET"])
@login_required()
def get_all():
    result = [{
        'id': 1,
        'patient_id': 1,
        'note': 'note test',
        'medication': 'medication test',
        'date': '2020-01-01'
    }, {
        'id': 2,
        'patient_id': 2,
        'note': 'note test2',
        'medication': 'medication test2',
        'date': '2020-01-01'
    }, {
        'id': 3,
        'patient_id': 3,
        'note': 'note test2',
        'medication': 'medication test2',
        'date': '2020-01-01'
    }]
    return make_response(jsonify({'ok': True, 'healthrecords': result}), 200)


@healthrecord.route('', methods=["POST"])
@login_required()
def create():
    # Todo
    return make_response(jsonify({'ok': True}), 200)


@healthrecord.route('/<healthrecord_id>', methods=["PUT"])
@login_required()
def change(healthrecord_id):
    # Todo
    return make_response(jsonify({'ok': True}), 200)


@healthrecord.route('/<healthrecord_id>', methods=["DELETE"])
@login_required()
def delete(healthrecord_id):
    # Todo
    return make_response(jsonify({'ok': True}), 200)
