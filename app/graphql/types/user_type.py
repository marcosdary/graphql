from strawberry.experimental.pydantic import type as pydantic_type
import strawberry
from app.dto.user import UserReadModel, UserListModel
    
@pydantic_type(UserReadModel)
class UserPublicType:
    name: strawberry.auto
    email: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto

@pydantic_type(UserReadModel, all_fields=True)
class UserPrivateType:
    pass

@pydantic_type(UserListModel, all_fields=True)
class UserListType:
    pass



