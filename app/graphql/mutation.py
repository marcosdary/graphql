import strawberry

from app.graphql.mutations.user_mutation import UserMutation
from app.graphql.mutations.admin_mutation import AdminMutation

@strawberry.type
class Mutation(UserMutation, AdminMutation):
    pass


