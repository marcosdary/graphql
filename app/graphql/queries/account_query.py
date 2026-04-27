import strawberry
from strawberry.exceptions import StrawberryGraphQLError

# Repository
from app.repositories.user_repository import UserRepository

# Permissions
from app.graphql.permissions import (
    SessionPermission, 
    ApiKeyPermission
)

# Responses
from app.graphql.utils import build_extensions

# Types
from app.graphql.types.user_type import UserPublicType

@strawberry.type
class AccountQuery:
        
    @strawberry.field(permission_classes=[ApiKeyPermission, SessionPermission])
    async def me(self, info) -> UserPublicType:
        try:
            user = info.context["user"]
            user_repo = UserRepository()

            data = await user_repo.get_user_by_id(user["userId"])
            
            return data
        
        except Exception as exc:
             raise StrawberryGraphQLError(
                message=str(exc),
                extensions=build_extensions(exc)
            )
        
    
    
