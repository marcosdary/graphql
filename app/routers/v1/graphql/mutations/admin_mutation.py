import strawberry

# Mutations
from app.routers.v1.graphql.mutations.admin_user_mutation import AdminUserMutation

@strawberry.type
class AdminMutation:
    
    @strawberry.field
    def users(self) -> AdminUserMutation:
        return AdminUserMutation()
    
  