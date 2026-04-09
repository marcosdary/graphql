import strawberry

# Repository
from app.repositories.user_repository import UserRepository

from app.services.cache import UserCacheService

# Permissions
from app.graphql.permissions import (
    RoutersProtectPermission
)

# Responses
from app.graphql.utils import build_response

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
class AdminQuery:

    @strawberry.field(permission_classes=[RoutersProtectPermission])
    async def listUsers(self, page: int = 1, limit: int = 10) -> ApiResponseType[UserListType, ApiErrorType]:
        try:
            user_cache_service = UserCacheService()

            data = await user_cache_service.list_users(page, limit)
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
        
    @strawberry.field(permission_classes=[RoutersProtectPermission])
    async def getByIdUser(self, userId: str) -> ApiResponseType[UserPrivateType, ApiErrorType]:
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
        except Exception:
            return build_response(False, exc=UnknownError("Erro interno do servidor."))
    
    
