import strawberry

# Inputs
from app.graphql.inputs import (
    ApiKeyInput,
)

# Types
from app.graphql.types import (
    ApiKeyType, 
    ApiErrorType, 
    ApiResponseType,
)

# Responses
from app.graphql.utils import build_response

# Permissions
from app.graphql.permissions import (
    SessionPermission, 
    RolePermission,
    ApiKeyPermission
)

# Services
from app.services import token 
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
class AdminApiKeyMutation:
    
    @strawberry.mutation(permission_classes=[SessionPermission])
    async def create(self, info, schema: ApiKeyInput) -> ApiResponseType[ApiKeyType, ApiErrorType]:
        try:
            api_key_service = token.ApiKeyService()
            user = info.context["user"]
            data = schema.to_pydantic()
            generate = await api_key_service.generate_api_key(data.expiration.value, **user)
            return build_response(True, generate)
        except (
            ApiError, DuplicateReviewError, EntityValidationError, ExpirationError,
            ForbiddenActionError, InvalidCredentialsException, InvalidFieldsException,
            NotFoundError, ProtectedRouteError, SessionError, TooManyRequestsError,
            UnprocessableEntity,
        ) as exc:
            return build_response(False, exc=exc)
        except Exception:
            return build_response(False, exc=UnknownError("Erro interno do servidor."))
    
    @strawberry.mutation(permission_classes=[SessionPermission])
    async def delete(self, key: str) -> ApiResponseType[bool, ApiErrorType]:
        try:
            api_key_service = token.ApiKeyService()
            await api_key_service.delete_api_key(token=key)
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