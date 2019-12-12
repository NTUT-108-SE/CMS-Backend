from . import invoice
import json
from app.modules.login_manager import login_required
from app.modules.schema import graphql
from flask_login import login_user, current_user
from flask import make_response, request
from flask.json import jsonify


@invoice.route('all', methods=["GET"])
@login_required()
def get_all_invoices():
    invoices = [
      {
        'financialNum': "0",
        'name': "前端測試帳號",
        'patientID': "A000000000",
        'createTime': "2019-10-20"
      },
      {
        'financialNum': "1",
        'name': "前端測試帳號",
        'patientID': "B000000000",
        'createTime': "2019-10-20"
      }
    ]
    return make_response(jsonify({'ok': True, 'invoices': invoices}), 200)


@invoice.route('', methods=["GET"])
@login_required()
def get_patient_invoices():
    patient_id = request.args.get('patientID', None)
    #Todo
    return make_response(jsonify({'ok': True, 'result': patient_id}), 200)

@invoice.route('<invoice_id>', methods=["GET"])
@login_required()
def get(invoice_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': invoice_id}), 200)

@invoice.route('<invoice_id>', methods=["PUT"])
@login_required()
def change(invoice_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': invoice_id + ' changed'}), 200)

@invoice.route('<invoice_id>', methods=["DELETE"])
@login_required()
def delete(invoice_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': invoice_id + ' deleted'}), 200)

@invoice.route('', methods=["POST"])
@login_required()
def create():
    #Todo
    return make_response(jsonify({'ok': True, 'result': 'created'}), 200)
