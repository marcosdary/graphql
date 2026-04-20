from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError

from app.services.token import ApiKeyService
from app.exceptions import InvalidFieldsException

class ApiKeyPermission(BasePermission):
   
    def __init__(self):
        self._api_key_service = ApiKeyService()
        super().__init__()

    async def has_permission(self, source, info, **kwargs) -> bool:
        try:
            if not info.context.get("api_key"):
                raise InvalidFieldsException("Rota protegida. Forneça sua API Key.")
            
            return True
        
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc), extensions={
                "typeError": exc.__class__.__name__,
                "statusCode": getattr(exc, "status_code", 500)
            })
        
    