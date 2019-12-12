from flask import Blueprint

invoice = Blueprint('invoice', __name__, url_prefix='/invoice')

from . import index
