from flask import Blueprint

healthrecord = Blueprint('healthrecord', __name__, url_prefix='/healthrecord')

from . import index
