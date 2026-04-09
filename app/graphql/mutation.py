import strawberry

from app.graphql.mutations import (
    UserMutation, 
    AdminMutation
)

@strawberry.type
class Mutation(UserMutation, AdminMutation):
    pass


