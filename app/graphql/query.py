import strawberry

from app.graphql.queries.user_query import UserQuery

@strawberry.type
class Query(UserQuery):
    pass

