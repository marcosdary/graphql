import strawberry

# Queries
from app.graphql.queries.admin_user_query import AdminUserQuery


@strawberry.type
class AdminQuery:

    @strawberry.field
    def users(self) -> AdminUserQuery:
        return AdminUserQuery()
    