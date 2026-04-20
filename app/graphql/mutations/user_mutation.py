import strawberry

# Repository
from app.repositories.user_repository import UserRepository

# Settings
from app.constants import SendType, ExpirationAt

# DTOs
from app.dto.user import UserUpdateModel

# Inputs
from app.graphql.inputs import (
    UserInput,
    UserUpdatePublicInput,
    UserLoginInput,
    Verify2FAInput,
    ForgotPasswordInput,
    UserResetPasswordInput
)

# Responses
from app.graphql.utils import build_response, create_session

# Permissions
from app.graphql.permissions import (
    SessionPermission, 
    ApiKeyPermission
)

# Types
from app.graphql.types import (
    UserPublicType, 
    SessionType, 
    TwoFactorAuthType, 
    PasswordResetType, 
    ApiErrorType,
    ApiResponseType
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
class UserMutation:

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def create(self, schema: UserInput) -> ApiResponseType[UserPublicType, ApiErrorType]:
        try:
            user = schema.to_pydantic()
            user_repo = UserRepository()
            
            data = await user_repo.create_user(user)
           
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


    @strawberry.mutation
    async def login(self, schema: UserLoginInput) -> ApiResponseType[TwoFactorAuthType, ApiErrorType]:
        try:
           
            user = schema.to_pydantic()

            user_repo = UserRepository()
            data = await user_repo.get_user_by_email_and_password(user)
           
            two_factor_auth_service = token.TwoFactorAuthService()

            create = await two_factor_auth_service.create_two_factor_token(
                userId=data.userId,
                role=data.role
            )
        
            return build_response(True, data=create)
        
        except (
            ApiError, DuplicateReviewError, EntityValidationError, ExpirationError,
            ForbiddenActionError, InvalidCredentialsException, InvalidFieldsException,
            NotFoundError, ProtectedRouteError, SessionError, TooManyRequestsError,
            UnprocessableEntity,
        ) as exc:
            return build_response(False, exc=exc)
        except Exception:
            return build_response(False, exc=UnknownError("Erro interno do servidor."))
    
    @strawberry.mutation
    async def verifyTwoFactor(self, schema: Verify2FAInput) -> ApiResponseType[SessionType, ApiErrorType]:
        try:
            two_fa = schema.to_pydantic()
            two_factor_auth_service = token.TwoFactorAuthService()
            data = await two_factor_auth_service.verify_two_factor_token(token=two_fa.token, number=two_fa.number)
            session_new = await create_session(
                userId=data.get("userId"), 
                role=data.get("role")
            )
            return build_response(True, data=session_new)
        
        except (
            ApiError, DuplicateReviewError, EntityValidationError, ExpirationError,
            ForbiddenActionError, InvalidCredentialsException, InvalidFieldsException,
            NotFoundError, ProtectedRouteError, SessionError, TooManyRequestsError,
            UnprocessableEntity,
        ) as exc:
            return build_response(False, exc=exc)
        except Exception:
            return build_response(False, exc=UnknownError("Erro interno do servidor."))

    @strawberry.mutation
    async def forgotPassword(self, schema: ForgotPasswordInput) -> ApiResponseType[PasswordResetType, ApiErrorType]:
        try:
            schema = schema.to_pydantic()

            password_reset_service = token.PasswordResetService()

            user_repo = UserRepository()
            data = await user_repo.get_user_by_email(schema)
    
            forgot = await password_reset_service.handle(
                action="forgot", 
                payload={
                    "userId": data.userId
                }
            )
            
            return build_response(True, data=forgot)
        except (
            ApiError, DuplicateReviewError, EntityValidationError, ExpirationError,
            ForbiddenActionError, InvalidCredentialsException, InvalidFieldsException,
            NotFoundError, ProtectedRouteError, SessionError, TooManyRequestsError,
            UnprocessableEntity,
        ) as exc:
            return build_response(False, exc=exc)
        except Exception:
            return build_response(False, exc=UnknownError("Erro interno do servidor."))

    @strawberry.mutation
    async def resetPassword(self, schema: UserResetPasswordInput) -> ApiResponseType[UserPublicType, ApiErrorType]:
        try:
            data_pydantic = schema.to_pydantic()
            password_reset_service = token.PasswordResetService()
            decode = await password_reset_service.handle(
                action="reset", 
                payload={"token": data_pydantic.token}
            )
            userId = decode.get("userId")
            
            user_repo = UserRepository()

            data = await user_repo.update_user( 
                user_update=UserUpdateModel(
                    userId=userId,
                    password=data_pydantic.password
                )
            )
            
            return build_response(True, data=data)
        
        except (
            ApiError, DuplicateReviewError, EntityValidationError, ExpirationError,
            ForbiddenActionError, InvalidCredentialsException, InvalidFieldsException,
            NotFoundError, ProtectedRouteError, SessionError, TooManyRequestsError,
            UnprocessableEntity,
        ) as exc:
            return build_response(False, exc=exc)
        except Exception as exc:
            return build_response(False, exc=UnknownError(f"Erro interno do servidor"))
          
    @strawberry.mutation(permission_classes=[ApiKeyPermission, SessionPermission])
    async def update(self, info, schema: UserUpdatePublicInput) -> ApiResponseType[UserPublicType, ApiErrorType]:  
        try:
            user = info.context["user"]
            user_update = schema.to_pydantic()
            user_repo = UserRepository()
            return build_response(
                success=True,
                data=await user_repo.update_user(user["userId"], user_update)
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
    async def delete(self, info) -> ApiResponseType[bool, ApiErrorType]:
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
