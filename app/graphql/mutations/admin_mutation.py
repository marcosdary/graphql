import strawberry

# Inputs
from app.graphql.inputs.api_key_input import (
    ApiKeyInput
)

# Types
from app.graphql.types.api_key_type import ApiKeyType
from app.graphql.types.api_error_type import ApiErrorType

# Responses
from app.graphql.base_type import ApiResponse
from app.graphql.utils import build_response

# Permissions
from app.graphql.permissions import session_permission

# Services
from app.services import token 


@strawberry.type
class AdminMutation:
    
    @strawberry.mutation(permission_classes=[session_permission.SessionPermission])
    def createApiKey(self, info, schema: ApiKeyInput) -> ApiResponse[ApiKeyType, ApiErrorType]:
        try:
            api_key_service = token.ApiKeyService()
            user = info.context["user"]
            data = schema.to_pydantic()
            generate = api_key_service.generate_api_key(data.expiration, **user)
            return build_response(True, generate)
        except Exception as exc:
            return build_response(False, exc=exc)

