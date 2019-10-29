from . import login
from modules.login_manager import User
from modules.schema import graphql
from flask_login import login_user, current_user
from flask import make_response, request
from flask.json import jsonify


@login.route('/', methods=["POST"])
def index():
    req_json = request.get_json(force=True)
    user = User(req_json['email'])
    if not user.is_authenticated() or user.get_password() == req_json['password']:
        return make_response(jsonify({'success': False, 'message': "vlidate failed."}), 403)

    login_user(user)
    rep_user = graphql.execute(
        '''
        query {
            user(email: "%s") {
                email
                name
                role
                image
                introduction
            }
        }
        ''' % user.get_id()
    ).data['user']
    return make_response(jsonify({'success': True, 'user': rep_user}), 200)
