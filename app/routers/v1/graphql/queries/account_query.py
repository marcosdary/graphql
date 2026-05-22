import strawberry
from strawberry.exceptions import StrawberryGraphQLError

# Repository
from app.repositories.user_repository import UserRepository

# Permissions
from app.routers.v1.graphql.permissions import (
    SessionPermission
)

# DTOs
from app.dto.user import UserRead

# Types
from app.routers.v1.graphql.types.user_type import UserPublicType

# Exceptions
from app.exceptions import (
    NotFoundError, 
)

@strawberry.type
class AccountQuery:
        
    @strawberry.field(permission_classes=[SessionPermission])
    async def me(self, info: strawberry.Info) -> UserPublicType:
        try:
            session = info.context.session
            user_id = info.context.user_id
            user_repo = UserRepository(session=session)
            data = await user_repo.get_user_by_id(user_id)
            
            return UserRead.model_validate(data)
        
        except NotFoundError as exc:
            raise StrawberryGraphQLError(message=str(exc))

        except Exception as exc:
            raise StrawberryGraphQLError(message=str(exc))
        
    
    
