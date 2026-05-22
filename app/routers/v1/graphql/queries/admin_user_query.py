import strawberry
from strawberry.http import GraphQLHTTPResponse
from strawberry.exceptions import StrawberryGraphQLError
from strawberry.field_extensions import InputMutationExtension

from typing import Optional

# Repository
from app.repositories.user_repository import UserRepository

# DTOs
from app.dto.user import UserList, UserRead

# Permissions
from app.routers.v1.graphql.permissions import (
    SessionPermission
)

# Inputs
from app.routers.v1.graphql.inputs import (
    PaginationInput,
    FilterByInput,
)

# Types
from app.routers.v1.graphql.types.user_type import UserListType, UserPrivateType

@strawberry.type
class AdminUserQuery:

    @strawberry.field(permission_classes=[SessionPermission], extensions=[InputMutationExtension()])
    async def list(
        self, 
        info: strawberry.Info,
        pagination: PaginationInput, 
        filterBy: Optional[FilterByInput] = None
    ) -> UserListType:
        try:
            session = info.context.session

            user_repo = UserRepository(session=session)
            
            pagination = pagination.to_pydantic()
            filter_by = filterBy.to_pydantic() if filterBy else None
            users = await user_repo.list_users(
                filter_by=filter_by, 
                pagination=pagination
            )
        
            return UserList.model_validate(users)
        
        except Exception as exc:
            raise StrawberryGraphQLError(message=str(exc))
                
    @strawberry.field(permission_classes=[SessionPermission])
    async def get_by_id(self, info: strawberry.Info, userId: str) -> UserPrivateType:
        try:
            session = info.context.session

            user_repo = UserRepository(session=session)

            user = await user_repo.get_user_by_id(id=userId)
            
            return UserRead.model_validate(user)

        except Exception as exc:
            raise StrawberryGraphQLError( message=str(exc))
        
        
    
    
