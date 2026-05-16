from strawberry.experimental.pydantic import type as pydantic_type
import strawberry
from app.dto.user import UserRead, UserList
from app.graphql.types.role_type import RoleType
    
@pydantic_type(UserRead)
class UserPublicType:
    name: strawberry.auto
    email: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto

@pydantic_type(UserRead, all_fields=True)
class UserPrivateType:
    pass

@pydantic_type(UserList, all_fields=True)
class UserListType:
    pass


