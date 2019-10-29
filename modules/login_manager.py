from app import login_manager
from modules.schema import graphql
from flask_login import current_user
from functools import wraps
import graphene

login_manager.session_protection = "strong"


class User:
    def __init__(self, email):
        query = '''
        query {
            user(email: "%s") {
                email
                name
                password
                role
            }
        }
        ''' % email
        self._user = graphql.execute(query).data['user'] or {
            'role': None,
            'name': None,
            'password': None,
            'email': None
        }

    def get_id(self):
        return self._user['email']

    def is_authenticated(self):
        return True if self._user.get('id') is not None else False

    def is_active(self):
        return True

    def is_anonymous(self):
        return not self.is_authenticated

    def get_urole(self):
        return self._user['role'] or "ANY"

    def get_name(self):
        return self._user['name']

    def get_password(self):
        return self._user['password']


def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if ((current_user.get_urole() != role) and (role != "ANY")):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


@login_manager.user_loader
def load_user(email):
    user = User(email)
    return user if user.is_authenticated else None
