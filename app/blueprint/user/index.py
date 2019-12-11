import json
from . import user
from app.modules.graphql import graphql
from flask import make_response, request
from flask.json import jsonify
from app.modules.login_manager import login_required


@user.route('all', methods=["GET"])
@login_required(role="Admin")
def get_all_users():
    users = graphql.execute(
        '''
    query {
      users {
            id
            name
            email
            image
            introduction
            role
        }
    }
    '''
    ).data['users']
    return make_response(jsonify({'ok': True, 'users': users}), 200)


@user.route('<user_id>', methods=["GET"])
@login_required()
def get_user(user_id):
    user = graphql.execute(
        '''
    query {
      user(id: "%s") {
            id
            name
            email
            image
            introduction
            role
        }
    }
    ''' % user_id
    ).data['user']
    if user == None:
        return make_response(jsonify({'ok': False}), 200)

    return make_response(jsonify({'ok': True, 'user': user}), 200)


@user.route('<user_id>', methods=["PUT"])
@login_required()
def change(user_id):
    # Todo
    return make_response(jsonify({'ok': True, 'result': user_id + ' changed'}), 200)


@user.route('<user_id>', methods=["DELETE"])
@login_required(role="Admin")
def delete(user_id):
    ok = graphql.execute(
        '''
    mutation {
        deleteUser(id: "%s"){
            ok
        }
    }
    ''' % user_id
    ).data['deleteUser']['ok']

    return make_response(jsonify({'ok': ok, 'result': user_id + ' deleted'}), 200)


@user.route('', methods=["POST"])
@login_required(role="Admin")
def create():
    form = json.loads(list(request.form.keys())[0])
    email = form.get('email')
    name = form.get('name')
    password = form.get('password')
    role = form.get('role')
    image = form.get('image', "")
    introduction = form.get('introduction', "")

    result = graphql.execute(
        '''
    mutation {
    createUser(userData: {email: "%s", name: "%s", password: "%s", role: "%s", image: "%s", introduction: "%s"}) {
        user {
            id
            name
            email
            image
            introduction
            role
        }
        ok
    }}''' % (email, name, password, role, image, introduction)
    ).data['createUser']

    ok = result['ok']

    if result['ok']:
        return make_response(jsonify({'ok': ok, 'user': result['user']}), 200)
    else:
        return make_response(jsonify({'ok': ok}), 400)