import strawberry
from strawberry.exceptions import StrawberryGraphQLError

# Inputs
from app.graphql.inputs import (
    UserPrivateInput,
    UserUpdatePrivateInput
)

# Types
from app.graphql.types.user_type import (
    UserPrivateType
)

# Repositories
from app.repositories import UserRepository

# Responses
from app.graphql.utils import build_extensions

# Permissions
from app.graphql.permissions import (
    SessionPermission, 
    RolePermission,
    ApiKeyPermission
)


@strawberry.type
class AdminUserMutation:
    

    @strawberry.mutation(permission_classes=[ApiKeyPermission, SessionPermission, RolePermission])
    async def create(self, info: strawberry.Info, schema: UserPrivateInput) -> UserPrivateType:
        try:
            user = schema.to_pydantic()
            
            user_repo = UserRepository()
            data = await user_repo.create_user(user)

            response = info.context["response"]
            response.headers["Last-Modified"] = data.createdAt.strftime("%a, %d %b %Y %H:%M:%S GMT")
            return data
        
        except Exception as exc:
            raise StrawberryGraphQLError(
                message=str(exc),
                extensions=build_extensions(exc)
            )
        
    @strawberry.mutation(permission_classes=[ApiKeyPermission, SessionPermission, RolePermission])
    async def update(self, info: strawberry.Info, schema: UserUpdatePrivateInput) -> UserPrivateType:  
        try:
            user_update = schema.to_pydantic()
            user_repo = UserRepository()
            data = await user_repo.update_user(user_update)
            response = info.context["response"]
            response.headers["Last-Modified"] = data.createdAt.strftime("%a, %d %b %Y %H:%M:%S GMT")
            return data
        
        except Exception as exc:
            raise StrawberryGraphQLError(
                message=str(exc),
                extensions=build_extensions(exc)
            )

    @strawberry.mutation(permission_classes=[ApiKeyPermission, SessionPermission, RolePermission])
    async def delete(self, userId: str) -> None:
        try:
            user_repo = UserRepository()
            await user_repo.delete_user(userId)
            return 
        
        except Exception as exc:
            raise StrawberryGraphQLError(
                message=str(exc),
                extensions=build_extensions(exc)
            )
    
 