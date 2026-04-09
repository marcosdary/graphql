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
            header = info.context["request"].headers
            auth = header.get("Authorization")

            if not auth:
                raise InvalidFieldsException("Rota protegida. Forneça sua API Key.")
            
            try:
                scheme, token = auth.split(" ")

                if scheme.lower() != "bearer":
                    return False
                
            except ValueError:
                return False
            
            await self._api_key_service.check_api_key(token)
            
            return True
        
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc), extensions={
                "typeError": exc.__class__.__name__,
                "statusCode": getattr(exc, "status_code", 500)
            })
        
    