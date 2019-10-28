from . import login
from .. import login_manager


@login.route('/', methods=["POST"])
def index():
    return "test"