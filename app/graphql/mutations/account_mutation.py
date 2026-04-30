import strawberry
from strawberry.exceptions import StrawberryGraphQLError

# Repository
from app.repositories.user_repository import UserRepository

# Inputs
from app.graphql.inputs import (
    UserUpdatePublicInput,
)

# Responses
from app.graphql.utils import build_extensions

# Permissions
from app.graphql.permissions import (
    SessionPermission, 
    ApiKeyPermission,
)

# Types
from app.graphql.types.user_type import UserPublicType

@strawberry.type
class AccountMutation:
          
    @strawberry.mutation(permission_classes=[ApiKeyPermission, SessionPermission])
    async def updateProfile(self, info: strawberry.Info, schema: UserUpdatePublicInput) -> UserPublicType:  
        try:
            user = info.context["user"]

            payload = schema.to_pydantic()
            user_update = payload.model_copy(update={"userId": user["userId"]})
            
            user_repo = UserRepository()

            return await user_repo.update_user(user_update)

        except Exception as exc:
             raise StrawberryGraphQLError(
                message=str(exc),
                extensions=build_extensions(exc)
            )
        

    @strawberry.mutation(permission_classes=[ApiKeyPermission, SessionPermission])
    async def deleteAccount(self, info) -> None:
        try:
            user = info.context["user"]
            user_repo = UserRepository()
            await user_repo.delete_user(user["userId"])
            return 
        
        except Exception as exc:
             raise StrawberryGraphQLError(
                message=str(exc),
                extensions=build_extensions(exc)
            )
