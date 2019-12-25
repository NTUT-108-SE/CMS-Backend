import json
from . import user
from app.modules.graphql import graphql
from flask import make_response, request
from flask.json import jsonify
from app.modules.login_manager import login_required
from flask_login import current_user


@user.route('/all', methods=["GET"])
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


@user.route('/<user_id>', methods=["GET"])
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


@user.route('/<user_id>', methods=["POST"])
@login_required(role="Admin")
def change_role(user_id):
    ok = False
    form = json.loads(list(request.form.keys())[0])
    role = form.get('role')
    if role == None or role not in ['Admin', 'Nurse', 'Doctor']:
        return make_response(jsonify({'ok': ok}), 400)

    ok = graphql.execute(
        '''
    mutation {
        mutateUser(userData: {id: "%s", role: "%s"}){
            ok
        }
    }
    ''' % (user_id, role)
    ).data['mutateUser']['ok']

    return make_response(jsonify({'ok': ok}), 200 if ok else 400)


@user.route('/<user_id>', methods=["DELETE"])
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

    return make_response(jsonify({'ok': ok}), 200 if ok else 400)


@user.route('', methods=["PUT"])
@login_required()
def change():
    form = json.loads(list(request.form.keys())[0])
    name = form.get('name', current_user.get_name())
    image = form.get('image', current_user.get_image())
    introduction = form.get('introduction', current_user.get_introduction())
    email = current_user.get_email()
    result = graphql.execute(
        '''
    mutation {
        mutateUser(userData: {email: "%s", name: "%s",image: "%s", introduction: "%s"}){
            user {
                id
                email
                name
                image
                introduction
                role
            }
            ok
        }
    }
    ''' % (email, name, image, introduction)
    ).data['mutateUser']
    ok = result['ok']
    user = result['user']
    return make_response(jsonify({'ok': ok, 'user': user}), 200 if ok else 400)


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

    if email == None or name == None or password == None or role == None:
        return make_response(jsonify({
            'ok': False,
        }), 400)

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

    return make_response(jsonify({'ok': ok, 'user': result['user']}), 200 if ok else 400)


@user.route('/change_password', methods=["POST"])
@login_required()
def change_password():
    form = json.loads(list(request.form.keys())[0])
    old_password = form.get('old_password')
    password = form.get('password')

    if password == None or old_password == None:
        return make_response(jsonify({'ok': False}), 400)

    ok = graphql.execute(
        '''
        query {
            login(email: "%s", password: "%s"){
                ok
            }
        }
        ''' % (current_user.get_email(), old_password)
    ).data['login']['ok']

    if ok is False:
        return make_response(jsonify({'ok': False}), 400)

    ok = graphql.execute(
        '''
    mutation {
        mutateUser(userData: {id: "%s", password: "%s"}){
            ok
        }
    }
    ''' % (current_user.get_id(), password)
    ).data['mutateUser']['ok']

    return make_response(jsonify({'ok': ok}), 200 if ok else 400)
