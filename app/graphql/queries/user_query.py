import strawberry
from typing import List

# Repository
from app.repositories.user_repository import UserRepository

# Permissions
from app.graphql.permissions import api_key_permission, session_permission

# Responses
from app.graphql.utils import build_response
from app.graphql.base_type import ApiResponse

# Types
from app.graphql.types.user_type import UserPrivateType, UserPublicType
from app.graphql.types.api_error_type import ApiErrorType

@strawberry.type
class UserQuery:

    @strawberry.field(permission_classes=[session_permission.SessionPermission])
    def listUsers(self) -> ApiResponse[List[UserPrivateType], ApiErrorType]:
        try:
            user_repo = UserRepository()
            return build_response(
                success=True,
                data=user_repo.list_users()
            )
        except Exception as exc:
            return build_response(False, exc=exc)
        
    @strawberry.field(permission_classes=[api_key_permission.ApiKeyPermission, session_permission.SessionPermission])
    def getUser(self, info) -> ApiResponse[UserPublicType, ApiErrorType]:
        try:
            user = info.context["user"]
            user_repo = UserRepository()
            return build_response(
                success=True,
                data=user_repo.get_user_by_id(user["userId"])
            )
        except Exception as exc:
            return build_response(False, exc=exc)
    
    
