from app import login_manager
from app.modules.graphql import graphql
from app.modules.domain.user import User
from flask_login import current_user
from functools import wraps
import graphene

login_manager.session_protection = "strong"


def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            urole = current_user.get_urole()
            if ((urole != role) and (role != "ANY")):
                if urole != "Admin":
                    return login_manager.unauthorized()
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


@login_manager.user_loader
def load_user(id):
    user = User(id=id)
    return user if user.is_authenticated else None
