from flask import Blueprint

medication = Blueprint('medication', __name__, url_prefix='/medication')

from . import index
