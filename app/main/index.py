from flask import make_response
from flask.json import jsonify

from . import main


@main.route('/', methods=["GET"])
def index():
    return make_response(jsonify({"success": True}), 200)
