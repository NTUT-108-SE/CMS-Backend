from flask import Blueprint

registration = Blueprint('registration', __name__, url_prefix='/registration')

from . import index
