from datetime import datetime, timedelta
import jwt
from random import randint

from app.services.token.base import BaseService
from app.config import settings
from app.constants import ExpirationTimes
from app.dto.password_reset import PasswordResetModel
from app.exceptions import UnprocessableEntity, InvalidFieldsException

class PasswordResetService(BaseService):
    def __init__(self):
        self._password_reset_key = settings.PASSWORD_RESET_KEY
        self._password_reset_expiration = ExpirationTimes.PASSWORD_RESET_EXPIRATION.value
        super().__init__()

    async def handle(self, action: str, payload: dict):

        if action == "forgot":
            return await self._create_password_reset_token(**payload)
        
        elif action == "reset":
            return await self._decode_reset_password(**payload)
        
        else:
            raise ValueError("Ação de redefinição de senha inválida")
        

    async def _create_password_reset_token(
        self, **kwargs
    ) -> PasswordResetModel:

        number = randint(100_000, 999_999)
        token = self._encode(kwargs, self._password_reset_key)

        await self._store_with_expiration(token, number, self._password_reset_expiration)

        return PasswordResetModel(
            token=token,
            number=number,
            expiresAt=datetime.now() + timedelta(seconds=self._password_reset_expiration)
        )

    async def _decode_reset_password(self, token: str) -> dict:
        data = await self._consume_or_none(token)

        if not data:
            raise UnprocessableEntity(
                "Token de verificação não encontrado. Faça um novo pedido."
            )
        return self._decode(token, self._password_reset_key)
        