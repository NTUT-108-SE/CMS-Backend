import graphene
from .query import Query
from .mutation import Mutation


class GraphQL(graphene.Schema):
    def __init__(self, query=None, mutation=None):
        super().__init__(query=query, mutation=mutation)
        self._query = query
        self._mutation = mutation


graphql = GraphQL(Query, Mutation)
