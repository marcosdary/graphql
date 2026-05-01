import strawberry
from strawberry.exceptions import StrawberryGraphQLError

# Repository
from app.repositories.user_repository import UserRepository

# Permissions
from app.graphql.permissions import (
    SessionPermission, 
    ApiKeyPermission
)

# DTOs
from app.dto.user import UserReadModel

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
class AccountQuery:
        
    @strawberry.field(permission_classes=[ApiKeyPermission, SessionPermission])
    async def me(self, info: strawberry.Info) -> UserPublicType:
        try:
            session = info.context["session"]
            user = info.context["user"]

            user_repo = UserRepository(session=session)

            data = await user_repo.get_user_by_id(user["userId"])
            
            return UserReadModel.model_validate(data)
        
        except NotFoundError as exc:
            raise StrawberryGraphQLError(message=str(exc))

        
        except Exception as exc:
            raise StrawberryGraphQLError(message=str(exc))
        
    
    
