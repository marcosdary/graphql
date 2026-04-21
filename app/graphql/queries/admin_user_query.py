import strawberry

from typing import Optional, Annotated

# Repository
from app.repositories.user_repository import UserRepository

from app.services.cache import UserCacheService

# Permissions
from app.graphql.permissions import (
    SessionPermission,
    RolePermission,
    ApiKeyPermission
)

# Responses
from app.graphql.utils import build_response

# Inputs
from app.graphql.inputs import (
    PaginationInput,
    FilterByInput,
)

# Types
from app.graphql.types import (
    UserPrivateType, 
    ApiErrorType,
    UserListType,
    ApiResponseType
)
from app.exceptions import (
    ApiError,
    DuplicateReviewError,
    EntityValidationError,
    ExpirationError,
    ForbiddenActionError,
    InvalidCredentialsException,
    InvalidFieldsException,
    NotFoundError,
    ProtectedRouteError,
    SessionError,
    TooManyRequestsError,
    UnknownError,
    UnprocessableEntity,
)

@strawberry.type
class AdminUserQuery:

    @strawberry.field(permission_classes=[ApiKeyPermission, SessionPermission])
    async def list(
        self, 
        pagination: PaginationInput, 
        filterBy: Optional[FilterByInput] = None
    ) -> ApiResponseType[UserListType, ApiErrorType]:
        try:
            user_repo = UserRepository()
            pagination = pagination.to_pydantic()
            filter_by = filterBy.to_pydantic() if filterBy else None
            data = await user_repo.list_users(
                filter_by=filter_by, 
                pagination=pagination
            )
            return build_response(
                success=True,
                data=data
            )
        except (
            ApiError, DuplicateReviewError, EntityValidationError, ExpirationError,
            ForbiddenActionError, InvalidCredentialsException, InvalidFieldsException,
            NotFoundError, ProtectedRouteError, SessionError, TooManyRequestsError,
            UnprocessableEntity,
        ) as exc:
            return build_response(False, exc=exc)
        except Exception as exc:
            print(exc)
            return build_response(False, exc=UnknownError("Erro interno do servidor."))
        
    @strawberry.field(permission_classes=[ApiKeyPermission, SessionPermission])
    async def getById(self, userId: str) -> ApiResponseType[UserPrivateType, ApiErrorType]:
        try:
            user_repo = UserRepository()

            data = await user_repo.get_user_by_id(user_id=userId)
            
            return build_response(
                success=True,
                data=data
            )
        except (
            ApiError, DuplicateReviewError, EntityValidationError, ExpirationError,
            ForbiddenActionError, InvalidCredentialsException, InvalidFieldsException,
            NotFoundError, ProtectedRouteError, SessionError, TooManyRequestsError,
            UnprocessableEntity,
        ) as exc:
            return build_response(False, exc=exc)
        except Exception as exc:
            return build_response(False, exc=UnknownError("Erro interno do servidor."))
        
    
    
