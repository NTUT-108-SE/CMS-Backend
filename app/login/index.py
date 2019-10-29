from . import login
import json
from modules.login_manager import User
from modules.schema import graphql
from flask_login import login_user, current_user
from flask import make_response, request
from flask.json import jsonify


@login.route('', methods=["POST"])
def login_index():
    form = json.loads(list(request.form.keys())[0])
    email = form.get('email')
    password = form.get('password')
    if email is None or password is None:
        return make_response(
            jsonify({
                'success': False,
                'message': "email or password should not be None"
            }), 401
        )

    user = User(email)
    if user.get_id() != email or user.get_password() != password:
        return make_response(jsonify({'success': False, 'message': "vlidate failed."}), 401)

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
