from pydantic import BaseModel, field_serializer
from datetime import datetime


class TwoFactorAuthModel(BaseModel):
    """
    Modelo de dados utilizado para autenticação de dois fatores (2FA).

    Este modelo representa as informações necessárias para um processo
    de 2FA, incluindo token, código numérico e data de expiração.

    Attributes:
        token (str): Token de verificação utilizado na autenticação de dois fatores.
        number (int): Código numérico enviado ao usuário para validação.
        expiresAt (datetime | None): Data e hora de expiração do token 2FA.
    """

    token: str
    number: int
    expiresAt: datetime | None = None

    @field_serializer("expiresAt", mode="plain")
    def serialize_dates(self, value: datetime | None) -> str | None:
        """
        Serializa objetos datetime em strings no formato ISO 8601.

        Args:
            value (datetime | None): Data/hora a ser serializada.

        Returns:
            str | None: Data/hora convertida para string ISO 8601 ou None
                caso o valor seja None.
        """
        if value is None:
            return None
        return value.isoformat()