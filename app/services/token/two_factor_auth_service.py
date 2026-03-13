from datetime import datetime, timedelta
from random import randint

from app.services.token.base import BaseService
from app.dto.two_factor_auth import TwoFactorAuthModel
from app.constants import settings
from app.exceptions import (
    InvalidCredentialsException,
    ExpirationError
)


class TwoFactorAuthService(BaseService):
    def __init__(self):
        self._admin_key = settings.KEY_ADMIN
        super().__init__()

    def create_two_factor_token(
        self, expiration: int = 600, **kwargs
    ) -> TwoFactorAuthModel:

        number = randint(100_000, 999_999)
        token = self._encode(kwargs, self._admin_key)

        self._store_with_expiration(token, number, expiration)

        return TwoFactorAuthModel(
            token=token,
            number=number,
            expiresAt=datetime.now() + timedelta(seconds=expiration)
        )

    def verify_two_factor_token(self, token: str, number: int) -> dict:
        data = self._get_or_none(token)

        if data is None:
            raise ExpirationError(
                "Token expirado ou removido. Faça um novo pedido."
            )

        if int(data) != number:
            raise InvalidCredentialsException(
                "Não identificado o número da credencial. Tente novamente."
            )

        decoded = self._decode(token, self._admin_key)
        self._delete(token)

        return decoded

    def delete_two_factor_token(self, token: str) -> None:
        self._delete(token)