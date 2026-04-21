import strawberry

# Repository
from app.repositories.user_repository import UserRepository

# Inputs
from app.graphql.inputs import (
    UserInput,
    UserUpdatePublicInput,
)

# Responses
from app.graphql.utils import build_response

# Permissions
from app.graphql.permissions import (
    SessionPermission, 
    ApiKeyPermission,
)

# Types
from app.graphql.types import (
    UserPublicType, 
    ApiErrorType,
    ApiResponseType
)

# Services
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
class AccountMutation:
          
    @strawberry.mutation(permission_classes=[ApiKeyPermission, SessionPermission])
    async def updateProfile(self, info, schema: UserUpdatePublicInput) -> ApiResponseType[UserPublicType, ApiErrorType]:  
        try:
            user = info.context["user"]

            payload = schema.to_pydantic()
            user_update = payload.model_copy(update={"userId": user["userId"]})
            
            user_repo = UserRepository()

            return build_response(
                success=True,
                data=await user_repo.update_user(user_update)
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
        

    @strawberry.mutation(permission_classes=[ApiKeyPermission, SessionPermission])
    async def deleteAccount(self, info) -> ApiResponseType[bool, ApiErrorType]:
        try:
            user = info.context["user"]
            user_repo = UserRepository()
            await user_repo.delete_user(user["userId"])
            return build_response(True)
        except (
            ApiError, DuplicateReviewError, EntityValidationError, ExpirationError,
            ForbiddenActionError, InvalidCredentialsException, InvalidFieldsException,
            NotFoundError, ProtectedRouteError, SessionError, TooManyRequestsError,
            UnprocessableEntity,
        ) as exc:
            return build_response(False, exc=exc)
        except Exception:
            return build_response(False, exc=UnknownError("Erro interno do servidor."))
