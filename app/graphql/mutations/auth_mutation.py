import strawberry
from strawberry.exceptions import StrawberryGraphQLError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
 
# Repository
from app.repositories.user_repository import UserRepository

# DTOs
from app.dto.user import UserUpdateModel, UserReadModel

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

# Responses
from app.graphql.utils import create_access_token

# Types
from app.graphql.types.two_factor_auth_type import TwoFactorAuthType
from app.graphql.types.password_reset_type import PasswordResetType
from app.graphql.types.user_type import UserPublicType
from app.graphql.types.session_type import SessionType


# Services
from app.services import token

# Exceptions
from app.exceptions import (
    DuplicateReviewError,
    NotFoundError,
    EntityValidationError,
    InvalidCredentialsException,
    ForbiddenActionError
)

@strawberry.type
class AuthMutation:

    @strawberry.mutation(permission_classes=[ApiKeyPermission])
    async def register(self, info: strawberry.Info, schema: UserInput) -> UserPublicType:
        try:
            session = info.context.session
            data = schema.to_pydantic()
            user_repo = UserRepository(session=session)
            
            user = await user_repo.create_user(data)
            
            await session.commit()
            return UserReadModel.model_validate(user)
        
        except IntegrityError:
            await session.rollback()
            raise StrawberryGraphQLError(message="Não foi possível criar o usuário.")

        except DuplicateReviewError as exc:
            raise StrawberryGraphQLError(message=str(exc))
        
        except Exception as exc:
            await session.rollback()
            raise StrawberryGraphQLError(message=str(exc))

    @strawberry.mutation
    async def login(self, info: strawberry.Info, schema: UserLoginInput) -> TwoFactorAuthType:
        try:
            session = info.context.session
            data = schema.to_pydantic()
            user_repo = UserRepository(session=session)

            user = await user_repo.get_user_by_email_and_password(data)
           
            two_factor_auth_service = token.TwoFactorAuthService()

            return await two_factor_auth_service.create_two_factor_token(
                user_id=user.user_id,
                role=user.role.value
            )
        
        except InvalidCredentialsException as exc:
            raise StrawberryGraphQLError(message=str(exc))
        
        except Exception as exc:
            raise StrawberryGraphQLError(message=str(exc))
    

    @strawberry.mutation
    async def verify_two_factor(self, schema: Verify2FAInput) -> SessionType:
        try:
            two_fa = schema.to_pydantic()
            two_factor_auth_service = token.TwoFactorAuthService()
            data = await two_factor_auth_service.verify_two_factor_token(token=two_fa.token, number=two_fa.number)
            session_new = create_access_token(
                user_id=data.get("sub"), 
                role=data.get("role")
            )
            return session_new
    
        except Exception as exc:
            raise StrawberryGraphQLError(message=str(exc))
        

    @strawberry.mutation
    async def forgot_password(self, info: strawberry.Info, schema: ForgotPasswordInput) -> PasswordResetType:
        try:
            session = info.context.session
            schema = schema.to_pydantic()

            password_reset_service = token.PasswordResetService()

            user_repo = UserRepository(session=session)
            user_id = await user_repo.get_user_by_email(schema)
    
            forgot = await password_reset_service.handle(
                action="forgot", 
                payload={
                    "user_id": user_id
                }
            )
            
            return forgot
        
        except InvalidCredentialsException as exc:
            raise StrawberryGraphQLError(message=str(exc))
        
        except Exception as exc:
            raise StrawberryGraphQLError(message=str(exc))


    @strawberry.mutation
    async def reset_password(self, info: strawberry.Info, schema: UserResetPasswordInput) -> UserPublicType:
        try:
            session = info.context.session

            data = schema.to_pydantic()
            password_reset_service = token.PasswordResetService()
            
            decode = await password_reset_service.handle(
                action="reset", 
                payload={"token": data.token}
            )
            user_id = decode.get("user_id")
            
            user_repo = UserRepository(session=session)

            user = await user_repo.update_user( 
                user_update=UserUpdateModel(
                    user_id=user_id,
                    password=data.password
                )
            )
            
            await session.commit()
            return UserReadModel.model_validate(user)
        
        except IntegrityError:
            await session.rollback()
            raise StrawberryGraphQLError(message="Não foi possível criar o usuário.")
        
        except DuplicateReviewError as exc:
            raise StrawberryGraphQLError(message=str(exc))
        
        except NotFoundError as exc:
            raise StrawberryGraphQLError(message=str(exc))
        
        except Exception as exc:
            await session.rollback()
            raise StrawberryGraphQLError(message=str(exc))
        
