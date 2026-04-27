import strawberry
from strawberry.http import GraphQLHTTPResponse
from strawberry.exceptions import StrawberryGraphQLError
from strawberry.field_extensions import InputMutationExtension

from typing import Optional

# Repository
from app.repositories.user_repository import UserRepository

# Permissions
from app.graphql.permissions import (
    SessionPermission,
    RolePermission,
    ApiKeyPermission
)

# Responses
from app.graphql.utils import build_extensions

# Inputs
from app.graphql.inputs import (
    PaginationInput,
    FilterByInput,
)

# Types
from app.graphql.types.user_type import UserListType, UserPrivateType


@strawberry.type
class AdminUserQuery:

    @strawberry.field(permission_classes=[ApiKeyPermission, SessionPermission, RolePermission], extensions=[InputMutationExtension()])
    async def list(
        self, 
        pagination: PaginationInput, 
        filterBy: Optional[FilterByInput] = None
    ) -> UserListType:
        try:
            user_repo = UserRepository()
            pagination = pagination.to_pydantic()
            filter_by = filterBy.to_pydantic() if filterBy else None
            data = await user_repo.list_users(
                filter_by=filter_by, 
                pagination=pagination
            )
            
            return data
        
        except Exception as exc:
            raise StrawberryGraphQLError(
                message=str(exc),
                extensions=build_extensions(exc)
            )
                
        
    @strawberry.field(permission_classes=[ApiKeyPermission, SessionPermission, RolePermission])
    async def getById(self, userId: str) -> UserPrivateType:
        try:
            user_repo = UserRepository()

            data = await user_repo.get_user_by_id(user_id=userId)
            
            return data

        except Exception as exc:
            raise StrawberryGraphQLError(
                message=str(exc),
                extensions=build_extensions(exc)
            )
        
        
    
    
