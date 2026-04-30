import strawberry
from strawberry.exceptions import StrawberryGraphQLError

# Inputs
from app.graphql.inputs import (
    ApiKeyInput,
)

# Types
from app.graphql.types.api_key_type import ApiKeyType

# Responses
from app.graphql.utils import build_extensions

# Permissions
from app.graphql.permissions import (
    SessionPermission, 
    RolePermission
)

# Services
from app.services import token 

@strawberry.type
class AdminApiKeyMutation:
    
    @strawberry.mutation(permission_classes=[SessionPermission, RolePermission])
    async def create(self, info, schema: ApiKeyInput) -> ApiKeyType:
        try:
            api_key_service = token.ApiKeyService()
            user = info.context["user"]
            data = schema.to_pydantic()
            
            return await api_key_service.generate_api_key(data.expiration.value, **user)
        
        except Exception as exc:
            raise StrawberryGraphQLError(message=str(exc))
    
    @strawberry.mutation(permission_classes=[SessionPermission, RolePermission])
    async def delete(self, key: str) -> None:
        try:
            api_key_service = token.ApiKeyService()
            await api_key_service.delete_api_key(token=key)
            return await api_key_service.delete_api_key(token=key)
        
        except Exception as exc:
            raise StrawberryGraphQLError(message=str(exc))