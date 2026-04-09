from datetime import datetime, timedelta

from app.services.token.base import BaseService
from app.config import settings
from app.dto.api_key import ApiKeyRead
from app.exceptions import ExpirationError


class ApiKeyService(BaseService):
    def __init__(self):
        self._create_api_key = settings.CREATE_API_KEY
        super().__init__()
    
    async def generate_api_key(self, exp: int, **kwargs) ->  ApiKeyRead:
    
        token = self._encode(kwargs, self._create_api_key)
        await self._store_with_expiration(token, kwargs["userId"], exp)
        expiresAt = datetime.now() + timedelta(seconds=exp)
        return ApiKeyRead(
            token=token,
            expiresAt=expiresAt
        )
    
    async def check_api_key(self, token: str) -> None:
        data = await self._fetch_or_none(token)
        if not data:
            raise ExpirationError("Token da API Key expirado ou removido. Faça um novo pedido")
        
    async def delete_api_key(self, token: str) -> None:
        await self._delete(key=token)