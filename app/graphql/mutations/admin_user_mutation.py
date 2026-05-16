import strawberry
from strawberry.exceptions import StrawberryGraphQLError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Core
from app.core.constants import Roles

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
from app.dto.user import (
    UserRead, 
    UserUpdateDB,
    UserCreateDB
)

# Repositories
from app.repositories import UserRepository, RoleRepository

# Permissions
from app.graphql.permissions import (
    SessionPermission
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
    

    @strawberry.mutation(permission_classes=[SessionPermission])
    async def create(self, info: strawberry.Info, schema: UserPrivateInput) -> UserPrivateType:
        try:
            session = info.context.session
           
            data = schema.to_pydantic()
            
            user_repo = UserRepository(session=session)
            
            role_id = None
            
            if data.role:
                if data.role == Roles.super_admin:
                    raise ForbiddenActionError("Tentativa de realizar uma ação proibida ou protegida.")
        
                role_repo = RoleRepository(session=session)
                role_id = await role_repo.get_role_by_name(data.role.value) if data.role else None

            data = UserCreateDB(
                name=data.name,
                email=data.email,
                password=data.password,
                role_id=role_id
            )

            user = await user_repo.create_user(data)
    
            await session.commit()
            await session.refresh(user, ["role"])
            
            return UserRead.model_validate(user)
        
        except IntegrityError:
            await session.rollback()
            raise StrawberryGraphQLError(message="Não foi possível criar o usuário.")

        except DuplicateReviewError as exc:
            raise StrawberryGraphQLError(message=str(exc))
        
        except Exception as exc:
            await session.rollback()
            raise StrawberryGraphQLError(message=str(exc))
        
    @strawberry.mutation(permission_classes=[SessionPermission])
    async def update(self, info: strawberry.Info, schema: UserUpdatePrivateInput) -> UserPrivateType:  
        try:
            session = info.context.session

            data = schema.to_pydantic()

            user_repo = UserRepository(session=session)
            
            role_id = None
            
            if data.role:
                if data.role == Roles.super_admin:
                    raise ForbiddenActionError("Tentativa de realizar uma ação proibida ou protegida.")
        
                role_repo = RoleRepository(session=session)
                role_id = await role_repo.get_role_by_name(data.role.value) if data.role else None

            data = UserUpdateDB(
                user_id=data.user_id,
                email=data.email,
                name=data.name,
                password=data.password,
                role_id=role_id
            )

            user = await user_repo.update_user(data)
            await session.commit()
            await session.refresh(user, ["role"])
            
            return UserRead.model_validate(user)
        
        except Exception as exc:
            await session.rollback()
            raise StrawberryGraphQLError(message=str(exc))

    @strawberry.mutation(permission_classes=[SessionPermission])
    async def delete(self, info: strawberry.Info, userId: str) -> None:
        try:
            session = info.context.session
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
    
 