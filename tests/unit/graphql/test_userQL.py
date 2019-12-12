import pytest
from app.modules.graphql import graphql


def test_list_user(db_user):
    users = graphql.execute('''
    query {
      users {
            name
        }
    }
    ''').data['users']
    assert users == [{"name": "User1"}, {"name": "User2"}]


def test_query_user(db_user):
    user = graphql.execute(
        '''
    query {
      user(email: "test@gmail.com") {
            name
        }
    }
    '''
    ).data['user']
    assert user == {"name": "User1"}


def test_query_user_by_id(db_user):
    id = graphql.execute(
        '''
    query {
        user(email: "test@gmail.com"){
            id
        }
    }'''
    ).data['user']['id']

    user = graphql.execute(
        '''
    query {
      user(id: "%s") {
            name
        }
    }
    ''' % id
    ).data['user']

    assert user == {"name": "User1"}


def test_query_user_not_found(db_user):
    user = graphql.execute(
        '''
    query {
      user(email: "") {
            name
        }
    }
    '''
    ).data['user']
    assert user == None

    user = graphql.execute('''
    query {
      user {
            name
        }
    }
    ''').data['user']
    assert user == None


def test_query_login(db_user):
    ok = graphql.execute(
        '''
    query {
        login(email: "test@gmail.com", password: "test"){
            ok
        }
    }
    '''
    ).data['login']['ok']
    assert ok == True


def test_failed_query_login(db_user):
    ok = graphql.execute(
        '''
    query {
        login(email: "test@gmail", password: "awefwef"){
            ok
        }
    }
    '''
    ).data['login']['ok']
    assert ok == False


def test_create_query_delete_user(db):
    ok = graphql.execute(
        '''
    mutation {
        createUser(userData: {email: "123@gmail.com", name: "123", password: "123", role: "Nurse"}){
            ok
        }
    }'''
    ).data['createUser']['ok']
    assert ok == True

    name = graphql.execute(
        '''
    query {
      user(email: "123@gmail.com") {
            name
        }
    }
    '''
    ).data["user"]["name"]

    assert name == "123"

    ok = graphql.execute(
        '''
    mutation {
        deleteUser(email: "123@gmail.com"){
            ok
        }
    }
    '''
    ).data['deleteUser']['ok']
    assert ok == True


def test_create_failed(db):
    ok = graphql.execute(
        '''
    mutation {
        createUser(userData: {email: "123@gmail.com", name: "123", password: "123", role: "Nurse"}){
            ok
        }
    }'''
    ).data['createUser']['ok']
    assert ok == True

    ok = graphql.execute(
        '''
    mutation {
        createUser(userData: {email: "123@gmail.com", name: "123", password: "123", role: "Nurse"}){
            ok
        }
    }'''
    ).data['createUser']['ok']
    assert ok == False


def test_mutate_user(db_user):
    result = graphql.execute(
        '''
    mutation {
        mutateUser(userData: {email: "test@gmail.com", name: "123"}){
            user {
                name
            }
            ok
        }
    }'''
    ).data['mutateUser']
    ok = result['ok']
    assert ok == True
    name = result['user']['name']
    assert name == '123'


def test_mutate_user_role(db_user):
    result = graphql.execute(
        '''
    mutation {
        mutateUser(userData: {email: "test@gmail.com", role:"Nurse"}){
            user {
                role
            }
            ok
        }
    }'''
    ).data['mutateUser']
    ok = result['ok']
    assert ok == True
    role = result['user']['role']
    assert role == 'Nurse'


def test_failed_mutate_user_role(db_user):
    result = graphql.execute(
        '''
    mutation {
        mutateUser(userData: {email: "test@gmail.com", role:"test"}){
            user {
                role
            }
            ok
        }
    }'''
    ).data['mutateUser']
    ok = result['ok']
    assert ok == False


def test_mutate_user_password(db_user):
    result = graphql.execute(
        '''
    mutation {
        mutateUser(userData: {email: "test@gmail.com", password:"test"}){
            ok
        }
    }'''
    ).data['mutateUser']
    ok = result['ok']
    assert ok == True


def test_delete_user_by_id(db_user):
    id = graphql.execute(
        '''
    query {
        user(email: "test@gmail.com"){
            id
        }
    }'''
    ).data['user']['id']

    ok = graphql.execute(
        '''
    mutation {
        deleteUser(id: "%s"){
            ok
        }
    }''' % id
    ).data['deleteUser']['ok']

    assert ok == True

    user = graphql.execute(
        '''
    query {
        user(email: "test@gmail.com"){
            id
        }
    }'''
    ).data['user']

    assert user == None


def test_delete_empty_user(db_user):
    ok = graphql.execute(
        '''
    mutation {
      deleteUser {
            ok
        }
    }
    '''
    ).data['deleteUser']['ok']
    assert ok == False
