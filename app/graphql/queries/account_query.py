import strawberry

# Repository
from app.repositories.user_repository import UserRepository

# Permissions
from app.graphql.permissions import (
    SessionPermission, 
    ApiKeyPermission
)

# Responses
from app.graphql.utils import build_response

# Types
from app.graphql.types import (
    UserPublicType, 
    ApiErrorType,
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
class AccountQuery:
        
    @strawberry.field(permission_classes=[ApiKeyPermission, SessionPermission])
    async def me(self, info) -> ApiResponseType[UserPublicType, ApiErrorType]:
        try:
            user = info.context["user"]
            user_repo = UserRepository()

            data = await user_repo.get_user_by_id(user["userId"])
            
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
    
    
