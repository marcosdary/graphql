import strawberry

# Mutations
from app.graphql.mutations.admin_api_key_mutation import AdminApiKeyMutation
from app.graphql.mutations.admin_user_mutation import AdminUserMutation

@strawberry.type
class AdminMutation:
    
    @strawberry.field
    def users(self) -> AdminUserMutation:
        return AdminUserMutation()
    
    @strawberry.field
    def apiKey(self) -> AdminApiKeyMutation:
        return AdminApiKeyMutation()
    