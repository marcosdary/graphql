from strawberry.experimental.pydantic import type as pydantic_type
import strawberry
from app.dto.user import UserReadModel, UserListModel
    
@pydantic_type(UserReadModel)
class UserPublicType:
    name: strawberry.auto
    email: strawberry.auto
    createdAt: strawberry.auto
    updatedAt: strawberry.auto

@pydantic_type(UserReadModel, all_fields=True)
class UserPrivateType:
    pass

@pydantic_type(UserListModel, all_fields=True)
class UserListType:
    pass


