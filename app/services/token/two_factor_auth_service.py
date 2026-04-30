from random import randint
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.services.token.base import BaseService
from app.dto.two_factor_auth import TwoFactorAuthModel

# Configs
from app.core.config import settings


# Constants
from app.core.constants import Roles, ExpirationTimes

# Exceptions
from app.exceptions import (
    InvalidCredentialsException,
    ExpirationError
)

class TwoFactorAuthService(BaseService):
    def __init__(self):
        self._two_factor_auth_key = settings.TWO_FACTOR_AUTH_KEY
        self._exp_two_factor_auth = ExpirationTimes.TWO_FA_EXPIRATION.value
        super().__init__()

    async def create_two_factor_token(
        self, userId: str, role: str
    ) -> TwoFactorAuthModel:
        sp = ZoneInfo("America/Sao_Paulo")
        iat = datetime.now(tz=sp)
        exp = iat + timedelta(minutes=self._exp_two_factor_auth)

        payload = {
            "sub": userId,
            "exp": exp.timestamp(),
            "scope": "pending",
            "iat": iat,
            "role": role
        }

        number = randint(100_000, 999_999)
        token = self._encode(payload, self._two_factor_auth_key)

        await self._store_with_expiration(token, number, self._exp_two_factor_auth * 60)

        return TwoFactorAuthModel(
            token=token,
            number=number
        )

    async def verify_two_factor_token(self, token: str, number: int) -> dict:
        value = await self._consume_or_none(token)
        
        if value is None:
            raise ExpirationError(
                "Token expirado ou removido. Faça um novo pedido."
            )

        if int(value) != number:
            raise InvalidCredentialsException(
                "Não identificado o número da credencial. Tente novamente."
            )

        payload = self._decode(token, self._two_factor_auth_key)
        return payload
