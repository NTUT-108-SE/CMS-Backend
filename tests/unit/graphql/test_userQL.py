import pytest
import graphene
from graphene_mongo import MongoengineObjectType
from modules.schema import graphql


def test_list_user(db_user):
    query = '''
    query {
      users {
            name
        }
    }
    '''
    result = graphql.execute(query)
    assert result.data['users'] == [{"name": "User1"}, {"name": "User2"}]


def test_query_user(db_user):
    query = '''
    query {
      user(email: "%s") {
            name
            password
        }
    }
    ''' % "test@gmail.com"
    result = graphql.execute(query)
    assert result.data['user'] == {"name": "User1", "password": "test"}
