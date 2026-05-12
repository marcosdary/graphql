import strawberry
from strawberry.exceptions import StrawberryGraphQLError
from datetime import datetime, timedelta, timezone


# Inputs
from app.graphql.inputs import (
    ApiKeyInput,
)

# Types
from app.graphql.types.api_key_type import ApiKeyType

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
            
            data = schema.to_pydantic()
            
            iat = datetime.now(timezone.utc).timestamp()
            exp = datetime.now(timezone.utc) + timedelta(seconds=data.expiration.value)

            return api_key_service.generate_api_key(
                type="api_key", 
                iat=int(iat),
                exp=int(exp.timestamp()),
                sub=info.context.user_id, 
                role=info.context.role
            )
        
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