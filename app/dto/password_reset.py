from pydantic import BaseModel, field_serializer
from datetime import datetime


class PasswordResetModel(BaseModel):
    """
    Modelo de dados utilizado para informações de redefinição de senha.

    Este modelo representa os dados retornados ou processados durante
    o fluxo de reset de senha, incluindo token de verificação, código numérico,
    mensagem de status e data de expiração.

    Attributes:
        token (str): Token utilizado para autorizar a redefinição de senha.
        number (int | None): Código numérico enviado ao usuário (opcional).
        message (str | None): Mensagem informativa ou de status (opcional).
        expiresAt (datetime | None): Data e hora de expiração do token (opcional).
    """

    token: str
    number: int | None = None
    message: str | None = None
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