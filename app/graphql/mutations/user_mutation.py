import strawberry
from random import randint

# Repository
from app.repositories.user_repository import UserRepository

# Settings
from app.constants import ExpirationTimes

# DTOs
from app.dto.user import UserUpdateModel

# Inputs
from app.graphql.inputs.user_input import (
    UserInput,
    UserPrivateInput,
    UserUpdateInput,
    UserLoginInput,
    Verify2FAInput,
    ForgotPasswordInput,
    VerifyCodeInput,
    UserResetPasswordInput
)

# Responses
from app.graphql.utils import build_response, create_session, send_email
from app.graphql.base_type import ApiResponse

# Permissions
from app.graphql.permissions import api_key_permission, session_permission

# Types
from app.graphql.types.user_type import UserPublicType, UserPrivateType
from app.graphql.types.session_type import SessionType
from app.graphql.types.two_factor_auth_type import TwoFactorAuthType
from app.graphql.types.password_reset_type import PasswordResetType
from app.graphql.types.api_error_type import ApiErrorType

# Services
from app.services import token

# Templates
from app.template import GeralActionTemplate, AdminNowTemplate

@strawberry.type
class UserMutation:

    @strawberry.mutation(permission_classes=[api_key_permission.ApiKeyPermission])
    def create(self, schema: UserInput) -> ApiResponse[UserPublicType, ApiErrorType]:
        try:
            user = schema.to_pydantic()
            user_repo = UserRepository()
            return build_response(
                success=True,
                data=user_repo.create_user(user)
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.mutation(permission_classes=[session_permission.SessionPermission])
    def createAdmin(self, schema: UserPrivateInput) -> ApiResponse[UserPrivateType, ApiErrorType]:
        try:
            user = schema.to_pydantic()
            
            user_repo = UserRepository()
            data = user_repo.create_user(user)

            send_email(
                "Novo usuário cadastrado ao sistema",
                schema.email,
                AdminNowTemplate(
                    title="Novo usuário",
                    header="Bem vindo, acesse o sistema para confirmar seu cadastro",
                    name=schema.name,
                    email=schema.email,
                    password=user.password
                )
            )

            return build_response(
                success=True,
                data=data
            )
        
        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.mutation
    def login(self, schema: UserLoginInput) -> ApiResponse[TwoFactorAuthType, ApiErrorType]:
        try:
            user = schema.to_pydantic()

            user_repo = UserRepository()
            data = user_repo.get_user_by_email_and_password(user)
            
            two_factor_auth_service = token.TwoFactorAuthService()
            encode = two_factor_auth_service.create_two_factor_token(
                expiration=ExpirationTimes.TWO_FA_EXPIRATION.value,
                userId=data.userId,
                role=data.role  
            )
            
            send_email(
                "Verificação de duas etapas", 
                data.email, 
                GeralActionTemplate(
                    title="Verificação de duas etapas",
                    header="Verificação da conta",
                    number=encode.number,
                    expiresAt=encode.expiresAt
                )          
            )
            
            return build_response(True, data=encode)
        
        except Exception as exc:
            return build_response(False, exc=exc)
        
    @strawberry.mutation
    def verifyTwoFactor(self, schema: Verify2FAInput) -> ApiResponse[SessionType, ApiErrorType]:
        try:
            two_fa = schema.to_pydantic()
            two_factor_auth_service = token.TwoFactorAuthService()
            data = two_factor_auth_service.verify_two_factor_token(token=two_fa.token, number=two_fa.number)
            session_new = create_session(
                userId=data.get("userId"), 
                role=data.get("role")
            )
            return build_response(True, data=session_new)
        
        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.mutation
    def forgotPassword(self, schema: ForgotPasswordInput) -> ApiResponse[PasswordResetType, ApiErrorType]:
        try:
            schema = schema.to_pydantic()

            password_reset_service = token.PasswordResetService()

            user_repo = UserRepository()
            data = user_repo.get_user_by_email(schema)
    
            generate = password_reset_service.handle(
                action="forgot", 
                payload={
                    "expiration": ExpirationTimes.PASSWORD_RESET_EXPIRATION.value, 
                    "userId": data.userId
                }
            )

            send_email(
                "Redefinição da Senha", 
                data.email, 
                GeralActionTemplate(
                    title="Redefinir Senha",
                    header="Verificação da conta",
                    number=generate.number,
                    expiresAt=generate.expiresAt
                )
            )
            return build_response(True, data=generate)
        except Exception as exc:
            return build_response(False, exc=exc)
        
    @strawberry.mutation
    def verifyCode(self, schema: VerifyCodeInput) -> ApiResponse[PasswordResetType, ApiErrorType]:
        try:
            data = schema.to_pydantic()
            password_reset_service = token.PasswordResetService()
            verify = password_reset_service.handle(
                action="verify", 
                payload={
                    "token": data.token, 
                    "number": data.number
                }
            )
            return build_response(True, data=verify)

        except Exception as exc:
            return build_response(False, exc=exc)

    @strawberry.mutation
    def resetPassword(self, schema: UserResetPasswordInput) -> ApiResponse[UserPublicType, ApiErrorType]:
        try:
            data_pydantic = schema.to_pydantic()
            password_reset_service = token.PasswordResetService()
            decode = password_reset_service.handle(
                action="reset", 
                payload={"token": data_pydantic.token}
            )
            userId = decode.get("userId")
            user_repo = UserRepository()
            return build_response(True,  data=user_repo.update_user(
                userId,
                UserUpdateModel(password=data_pydantic.password)
            ))
        
        except Exception as exc:
            return build_response(False, exc=exc)
          
    @strawberry.mutation(permission_classes=[api_key_permission.ApiKeyPermission, session_permission.SessionPermission])
    def update(self, info, schema: UserUpdateInput) -> ApiResponse[UserPublicType, ApiErrorType]:  
        try:
            user = info.context["user"]
            user_update = schema.to_pydantic()
            user_repo = UserRepository()
            return build_response(
                success=True,
                data=user_repo.update_user(user["userId"], user_update)
            )
        except Exception as exc:
            return build_response(False, exc=exc)
        
    @strawberry.mutation(permission_classes=[api_key_permission.ApiKeyPermission, session_permission.SessionPermission])
    def delete(self, info) -> ApiResponse[bool, ApiErrorType]:
        try:
            user = info.context["user"]
            user_repo = UserRepository()
            user_repo.delete_user(user["userId"])
            return build_response(True)
        except Exception as exc:
            return build_response(False, exc=exc)
