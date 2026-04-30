import strawberry
from strawberry.exceptions import StrawberryGraphQLError

# Repository
from app.repositories.user_repository import UserRepository

# DTOs
from app.dto.user import UserUpdateModel

# Inputs
from app.graphql.inputs import (
    UserInput,
    UserLoginInput,
    Verify2FAInput,
    ForgotPasswordInput,
    UserResetPasswordInput
)

# Permissions
from app.graphql.permissions import (
    ApiKeyPermission,
)

# Constants
from app.core.constants import ExpirationTimes


# Responses
from app.graphql.utils import build_extensions, create_session

# Types
from app.graphql.types.two_factor_auth_type import TwoFactorAuthType
from app.graphql.types.password_reset_type import PasswordResetType
from app.graphql.types.user_type import UserPublicType
from app.graphql.types.session_type import SessionType


# Services
from app.services import token

@strawberry.type
class AuthMutation:

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def register(self, info: strawberry.Info, schema: UserInput) -> UserPublicType:
        try:
            user = schema.to_pydantic()
            user_repo = UserRepository()
            
            data = await user_repo.create_user(user)

            response = info.context["response"]
            response.headers["Last-Modified"] = data.createdAt.strftime("%a, %d %b %Y %H:%M:%S GMT")
            return data
        
        except Exception as exc:
            raise StrawberryGraphQLError(
                message=str(exc),
                extensions=build_extensions(exc)
            )

    @strawberry.mutation
    async def login(self, schema: UserLoginInput) -> TwoFactorAuthType:
        try:
            user = schema.to_pydantic()
            user_repo = UserRepository()
            data = await user_repo.get_user_by_email_and_password(user)
           
            two_factor_auth_service = token.TwoFactorAuthService()

            return await two_factor_auth_service.create_two_factor_token(
                userId=data.userId,
                role=data.role
            )
        
        except Exception as exc:
            raise StrawberryGraphQLError(
                message=str(exc),
                extensions=build_extensions(exc)
            )
    

    @strawberry.mutation
    async def verifyTwoFactor(self, schema: Verify2FAInput) -> SessionType:
        try:
            two_fa = schema.to_pydantic()
            two_factor_auth_service = token.TwoFactorAuthService()
            data = await two_factor_auth_service.verify_two_factor_token(token=two_fa.token, number=two_fa.number)
            session_new = await create_session(
                userId=data.get("sub"), 
                role=data.get("role")
            )
            return session_new
    
        except Exception as exc:
            raise StrawberryGraphQLError(
                message=str(exc),
                extensions=build_extensions(exc)
            )


    @strawberry.mutation
    async def forgotPassword(self, schema: ForgotPasswordInput) -> PasswordResetType:
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
            
            return forgot
        
        except Exception as exc:
            raise StrawberryGraphQLError(
                message=str(exc),
                extensions=build_extensions(exc)
            )


    @strawberry.mutation
    async def resetPassword(self, schema: UserResetPasswordInput) -> UserPublicType:
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
            
            return data
        
        except Exception as exc:
            raise StrawberryGraphQLError(
                message=str(exc),
                extensions=build_extensions(exc)
            )
        
