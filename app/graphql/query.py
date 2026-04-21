import strawberry

from app.graphql.queries import AccountQuery, AdminQuery



@strawberry.type
class Query:
    
    @strawberry.field
    def user(self) -> AccountQuery: 
        return AccountQuery()

    @strawberry.field
    def admin(self) -> AdminQuery: 
        return AdminQuery()

