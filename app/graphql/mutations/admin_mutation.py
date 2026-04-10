import strawberry

# Inputs
from app.graphql.inputs import (
    ApiKeyInput,
    UserPrivateInput,
    UserUpdatePrivateInput
)

# Types
from app.graphql.types import (
    ApiKeyType, 
    ApiErrorType, 
    ApiResponseType,
    UserPrivateType,
)

# Repositories
from app.repositories import UserRepository

# Responses
from app.graphql.utils import build_response

# Permissions
from app.graphql.permissions import RoutersProtectPermission

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
class AdminMutation:
    
    @strawberry.mutation(permission_classes=[RoutersProtectPermission])
    async def createApiKey(self, info, schema: ApiKeyInput) -> ApiResponseType[ApiKeyType, ApiErrorType]:
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

    @strawberry.mutation(permission_classes=[RoutersProtectPermission])
    async def createUserByAdmin(self, schema: UserPrivateInput) -> ApiResponseType[UserPrivateType, ApiErrorType]:
        try:
            user = schema.to_pydantic()
            
            user_repo = UserRepository()
            data = await user_repo.create_user(user)
            """
            await send_notification_to_email(
                recipient_email=data.email,
                action_link="www.google.com",
                send_type=SendType.REGISTER
            )
            """
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
        
    @strawberry.mutation(permission_classes=[RoutersProtectPermission])
    async def updateUserByAdmin(self, schema: UserUpdatePrivateInput) -> ApiResponseType[UserPrivateType, ApiErrorType]:  
        try:
            user_update = schema.to_pydantic()
            user_repo = UserRepository()
            data = await user_repo.update_user(user_update)
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

    @strawberry.mutation(permission_classes=[RoutersProtectPermission])
    async def deleteUserByAdmin(self, userId: str) -> ApiResponseType[bool, ApiErrorType]:
        try:
            user_repo = UserRepository()
            await user_repo.delete_user(userId)
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
    
    @strawberry.mutation(permission_classes=[RoutersProtectPermission])
    async def deleteApiKey(self, key: str) -> ApiResponseType[bool, ApiErrorType]:
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