import strawberry

from app.routers.v1.graphql.mutations import (
    AccountMutation, 
    AdminMutation,
    AuthMutation
)

@strawberry.type
class Mutation:
    
    @strawberry.field
    def admin(self) -> AdminMutation: 
        return AdminMutation()

    @strawberry.field
    def user(self) -> AccountMutation: 
        return AccountMutation()
    
    @strawberry.field
    def auth(self) -> AuthMutation:
        return AuthMutation()

