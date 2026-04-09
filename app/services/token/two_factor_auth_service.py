from datetime import datetime, timedelta
from random import randint

from app.services.token.base import BaseService
from app.dto.two_factor_auth import TwoFactorAuthModel
from app.config import settings
from app.constants import ExpirationTimes
from app.exceptions import (
    InvalidCredentialsException,
    ExpirationError
)

class TwoFactorAuthService(BaseService):
    def __init__(self):
        self._two_factor_auth_key = settings.TWO_FACTOR_AUTH_KEY
        self._expiration_two_factor_auth = ExpirationTimes.TWO_FA_EXPIRATION.value
        super().__init__()

    async def create_two_factor_token(
        self, **kwargs
    ) -> TwoFactorAuthModel:

        number = randint(100_000, 999_999)
        token = self._encode(kwargs, self._two_factor_auth_key)

        await self._store_with_expiration(token, number, self._expiration_two_factor_auth)

        return TwoFactorAuthModel(
            token=token,
            number=number,
            expiresAt=datetime.now() + timedelta(seconds=self._expiration_two_factor_auth)
        )

    async def verify_two_factor_token(self, token: str, number: int) -> dict:
        data = await self._consume_or_none(token)

        if data is None:
            raise ExpirationError(
                "Token expirado ou removido. Faça um novo pedido."
            )

        if int(data) != number:
            raise InvalidCredentialsException(
                "Não identificado o número da credencial. Tente novamente."
            )

        decoded = self._decode(token, self._two_factor_auth_key)

        return decoded
