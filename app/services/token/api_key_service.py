from datetime import datetime, timedelta

from app.services.token.base import BaseService
from app.constants import settings, ExpirationApiKey
from app.dto.api_key import ApiKeyRead
from app.exceptions import InvalidFieldsException, ExpirationError


class ApiKeyService(BaseService):
    def __init__(self):
        self._create_api_key = settings.CREATE_API_KEY
        super().__init__()

    def _get_expiration(self, exp) -> str:
        if not isinstance(exp, ExpirationApiKey):
            raise InvalidFieldsException("Campo informado inválido. Forneça o campo incorreto.")
        return exp.value
    
    def generate_api_key(self, expiration: str, **kwargs) ->  ApiKeyRead:
        exp = self._get_expiration(expiration)
        token = self._encode(kwargs, self._create_api_key)
        self._store_with_expiration(token, kwargs["userId"], exp)
        expiresAt = datetime.now() + timedelta(seconds=exp)
        return ApiKeyRead(
            token=token,
            expiresAt=expiresAt
        )
    
    def check_api_key(self, token: str) -> None:
        data = self._get_or_none(token)
        if not data:
            raise ExpirationError("Token da API Key expirado ou removido. Faça um novo pedido")