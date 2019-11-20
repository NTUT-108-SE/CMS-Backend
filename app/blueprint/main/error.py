from flask import make_response
from flask.json import jsonify

from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"error": "Page not found!"}), 404)
