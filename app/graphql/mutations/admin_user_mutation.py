import strawberry
from strawberry.exceptions import StrawberryGraphQLError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Inputs
from app.graphql.inputs import (
    UserPrivateInput,
    UserUpdatePrivateInput
)

# Types
from app.graphql.types.user_type import (
    UserPrivateType
)

# DTOs
from app.dto.user import UserReadModel

# Repositories
from app.repositories import UserRepository

# Permissions
from app.graphql.permissions import (
    SessionPermission, 
    RolePermission,
    ApiKeyPermission
)

# Exceptions
from app.exceptions import (
    DuplicateReviewError,
    NotFoundError,
    EntityValidationError,
    InvalidCredentialsException,
    ForbiddenActionError
)


@strawberry.type
class AdminUserMutation:
    

    @strawberry.mutation(permission_classes=[ApiKeyPermission, SessionPermission, RolePermission])
    async def create(self, info: strawberry.Info, schema: UserPrivateInput) -> UserPrivateType:
        try:
            session = info.context["session"]
           
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
        
    @strawberry.mutation(permission_classes=[ApiKeyPermission, SessionPermission, RolePermission])
    async def update(self, info: strawberry.Info, schema: UserUpdatePrivateInput) -> UserPrivateType:  
        try:
            session = info.context["session"]

            data = schema.to_pydantic()
            user_repo = UserRepository(session=session)
            user = await user_repo.update_user(data)
            await session.commit()
            return UserReadModel.model_validate(user)
        
        except Exception as exc:
            await session.rollback()
            raise StrawberryGraphQLError(message=str(exc))

    @strawberry.mutation(permission_classes=[ApiKeyPermission, SessionPermission, RolePermission])
    async def delete(self, info: strawberry.Info, userId: str) -> None:
        try:
            session = info.context["session"]
            user_repo = UserRepository(session=session)
            await user_repo.delete_user(userId)
            await session.commit()
            return 
        
        except SQLAlchemyError as exc:
            await session.rollback()
            raise StrawberryGraphQLError(message=str(exc))

        except NotFoundError as exc:
            await session.rollback()
            raise StrawberryGraphQLError(message=str(exc))
        
        except Exception as exc:
            await session.rollback()
            raise StrawberryGraphQLError(message=str(exc))
    
 