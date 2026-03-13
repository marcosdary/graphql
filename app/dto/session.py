from datetime import datetime
from pydantic import BaseModel, field_serializer


class SessionModel(BaseModel):
    """
    Modelo de dados que representa uma sessão de usuário.

    Este modelo é utilizado para armazenar e retornar informações
    sobre sessões ativas, incluindo identificador, data de criação
    e data de expiração.

    Attributes:
        sessionId (str): Identificador único da sessão.
        createdAt (datetime): Data e hora de criação da sessão.
        expiresAt (datetime): Data e hora de expiração da sessão.
    """

    sessionId: str
    createdAt: datetime
    expiresAt: datetime

    @field_serializer("createdAt", "expiresAt", mode="plain")
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