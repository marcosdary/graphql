import strawberry

from app.graphql.queries import UserQuery, AdminQuery

@strawberry.type
class Query(UserQuery, AdminQuery):
    pass

