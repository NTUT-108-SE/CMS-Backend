import pytest
import graphene
from graphene_mongo import MongoengineObjectType
from modules.schema import Query


def test_list_user(db_user):
    schema = graphene.Schema(query=Query)
    query = '''
    query {
      users {
            name
        }
    }
    '''
    result = schema.execute(query)
    assert result.data['users'] == [{"name": "User1"}, {"name": "User2"}]


def test_query_user(db_user):
    schema = graphene.Schema(query=Query)
    query = '''
    query {
      user(email:"test@gmail.com") {
            name
            password
        }
    }
    '''
    result = schema.execute(query)
    assert result.data['user'] == {"name": "User1", "password": "test"}
