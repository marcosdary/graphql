from datetime import datetime, timedelta
from random import randint

from app.services.token.base import BaseService
from app.constants import settings
from app.dto.password_reset import PasswordResetModel
from app.exceptions import UnprocessableEntity

class PasswordResetService(BaseService):
    def __init__(self):
        self._password_reset_key = settings.PASSWORD_RESET_KEY
        super().__init__()

    def handle(self, action: str, payload: dict):

        if action == "forgot":
            return self._create_password_reset_token(**payload)
        
        elif action == "verify":
            return self._verify_password_reset_token(**payload)
        
        elif action == "reset":
            return self._decode_reset_password(**payload)
        
        else:
            raise ValueError("Invalid password reset action")
        

    def _create_password_reset_token(
        self, expiration: int = 3600, **kwargs
    ) -> PasswordResetModel:

        number = randint(100_000, 999_999)
        token = self._encode(kwargs, self._password_reset_key)

        self._store_with_expiration(token, number, expiration)

        return PasswordResetModel(
            message="Novo pedido de recuperação criado. Redefina sua senha",
            token=token,
            number=number,
            expiresAt=datetime.now() + timedelta(seconds=expiration)
        )

    def _verify_password_reset_token(self, token: str, number: int) -> PasswordResetModel:
        data = self._get_or_none(token)

        if data is None:
            raise UnprocessableEntity(
                "Token de verificação não encontrado. Faça um novo pedido."
            )

        if int(data) != number:
            raise UnprocessableEntity("Número de verificação incorreto.")

        self._delete(token)

        return PasswordResetModel(token=token)

    def _decode_reset_password(self, token: str) -> dict:
        return self._decode(token, self._password_reset_key)
    