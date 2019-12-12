from . import login
import json
from app.modules.graphql import graphql
from app.modules.domain.user import User
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
                'ok': False,
                'message': "email or password should not be None"
            }), 401
        )

    ok = graphql.execute(
        '''
    query {
        login(email: "%s", password:"%s"){
            ok
        }
    }
    ''' % (email, password)
    ).data['login']['ok']

    if ok != True:
        return make_response(jsonify({'ok': ok, 'message': "vlidate failed."}), 401)

    user = User(email=email)
    login_user(user)
    rep_user = graphql.execute(
        '''
        query {
            user(id: "%s") {
                email
                name
                role
                image
                introduction
            }
        }
        ''' % user.get_id()
    ).data['user']
    return make_response(jsonify({'ok': ok, 'user': rep_user}), 200)
