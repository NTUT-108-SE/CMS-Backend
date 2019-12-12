from flask import make_response
from flask.json import jsonify
from flask_login import logout_user
from app.modules.login_manager import login_required
from . import main


@main.route('/', methods=["GET"])
def index():
    return make_response(jsonify({"ok": True}), 200)


@main.route('/logout')
@login_required()
def logout():
    logout_user()
    return make_response(jsonify({"ok": True}), 200)


@main.route('/check')
@login_required()
def check():
    return make_response(jsonify({"ok": True}), 200)
