from app.services.token.base import BaseService
from app.core.config import settings
from app.dto.api_key import ApiKeyRead


class ApiKeyService(BaseService):
    def __init__(self):
        self._create_api_key = settings.CREATE_API_KEY
        super().__init__()
    
    def generate_api_key(self, **kwargs) ->  ApiKeyRead:
        token = self._encode(kwargs, self._create_api_key)
        return ApiKeyRead(
            token=token
        )
    
    def decode_api_key(self, token: str) -> dict:
        return self._decode(token, self._create_api_key)
        
    async def delete_api_key(self, token: str) -> None:
        await self._delete(key=token)