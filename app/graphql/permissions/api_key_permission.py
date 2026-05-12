from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError
from datetime import datetime, timezone
from jwt.exceptions import InvalidSignatureError


from app.services.token import ApiKeyService
from app.exceptions import ExpirationError, ForbiddenActionError


class ApiKeyPermission(BasePermission):

    def __init__(self):
        self._api_key_service = ApiKeyService()
        super().__init__()

    async def has_permission(self, source, info, **kwargs) -> bool:
        api_key = info.context.api_key
        if not api_key:
            return False

        try:
            payload: dict = self._api_key_service.decode_api_key(api_key)
            current = int(datetime.now(timezone.utc).timestamp())
            exp = payload.get("exp")

            if not exp > current:
                raise ExpirationError("Recurso ou sessão expirada.")
            
            return True
        
        except InvalidSignatureError:
            raise ForbiddenActionError("Tentativa de realizar uma ação proibida ou protegida.")

        except Exception as exc:
            raise exc

