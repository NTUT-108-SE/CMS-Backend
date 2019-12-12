from . import management
import json
from app.modules.login_manager import login_required
from flask import make_response, request
from flask.json import jsonify


@management.route('', methods=["GET"])
@login_required()
def get():
    #Todo
    return make_response(jsonify({'ok': True}), 200)


@management.route('information', methods=["PUT"])
@login_required()
def change():
    #Todo
    return make_response(jsonify({'ok': True, 'result': 'information changed'}), 200)


@management.route('announcements', methods=["GET"])
@login_required()
def get_announcements():
    announcements = [{
        'bulletinNum': "0",
        'bulletinDate': "2019-10-20",
        'title': "測試文章",
        'ctr': "1"
    }, {
        'bulletinNum': "1",
        'bulletinDate': "2019-10-20",
        'title': "測試文章2",
        'ctr': "10"
    }]
    return make_response(jsonify({'ok': True, 'announcements': announcements}), 200)


@management.route('announcement/<announcements_id>', methods=["GET"])
@login_required()
def get_announcement(announcements_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': announcements_id}), 200)


@management.route('announcement', methods=["POST"])
@login_required()
def create_announcement():
    #Todo
    return make_response(jsonify({'ok': True, 'result': 'created'}), 200)


@management.route('announcement/<announcement_id>', methods=["PUT"])
@login_required()
def change_announcement(announcement_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': announcement_id + ' changed'}), 200)


@management.route('announcement/<announcement_id>', methods=["DELETE"])
@login_required()
def delete_announcement(announcement_id):
    #Todo
    return make_response(jsonify({'ok': True, 'result': announcement_id + ' deleted'}), 200)
