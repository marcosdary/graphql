import strawberry
from strawberry.exceptions import StrawberryGraphQLError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Repository
from app.repositories.user_repository import UserRepository

# DTOs
from app.dto.user import UserRead

# Inputs
from app.graphql.inputs import (
    UserUpdatePublicInput,
)

# Permissions
from app.graphql.permissions import (
    SessionPermission, 
    ApiKeyPermission,
)

# Types
from app.graphql.types.user_type import UserPublicType

# Exceptions
from app.exceptions import (
    DuplicateReviewError,
    NotFoundError,
    EntityValidationError,
    InvalidCredentialsException,
    ForbiddenActionError
)

@strawberry.type
class AccountMutation:
          
    @strawberry.mutation(permission_classes=[ApiKeyPermission, SessionPermission])
    async def update_profile(self, info: strawberry.Info, schema: UserUpdatePublicInput) -> UserPublicType:  
        try:
            session = info.context.session
            user = info.context["user"]

            payload = schema.to_pydantic()
            user_update = payload.model_copy(update={"userId": user["userId"]})
            
            user_repo = UserRepository(session=session)

            updated = await user_repo.update_user(user_update)

            await session.commit()

            return UserRead.model_validate(updated)
        
        except IntegrityError:
            await session.rollback()
            raise StrawberryGraphQLError(message="Não foi possível criar o usuário.")
        
        except DuplicateReviewError as exc:
            raise StrawberryGraphQLError(message=str(exc))
        
        except NotFoundError as exc:
            raise StrawberryGraphQLError(message=str(exc))

        except Exception as exc:
            raise StrawberryGraphQLError(message=str(exc))
        

    @strawberry.mutation(permission_classes=[ApiKeyPermission, SessionPermission])
    async def delete_account(self, info) -> None:
        try:
            session = info.context.session
            user = info.context["user"]
            userId = user["sub"]
            user_repo = UserRepository(session=session)
            await user_repo.delete_user(userId)
            await session.commit()
            return 
        
        except SQLAlchemyError as exc:
            raise StrawberryGraphQLError(message=str(exc))

        except NotFoundError as exc:
            raise StrawberryGraphQLError(message=str(exc))
        
        except Exception as exc:
            raise StrawberryGraphQLError(message=str(exc))
