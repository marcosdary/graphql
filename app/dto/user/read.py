from datetime import datetime
from pydantic import field_serializer
from typing import Optional

# Base Model Pydantic
from app.dto.user.model import UserModel
from app.dto.role import RoleRead

# Settings
from app.core.config import settings


class UserRead(UserModel):
    """
    Modelo de leitura de dados de usuários.

    Esta classe estende UserModel e é utilizada para representar
    os dados de um usuário de forma completa para leitura, incluindo
    informações de auditoria e status de exclusão.

    Attributes:
        userId (str): Identificador único do usuário.
        name (str): Nome do usuário.
        email (str): Endereço de e-mail do usuário.
        password (str): Senha do usuário (criptografada).
        role (str): Papel do usuário no sistema (ex: "user" ou "admin").
        isDeleted (bool): Indica se o usuário foi marcado como excluído.
        createdAt (datetime): Data e hora de criação do usuário.
        updatedAt (datetime): Data e hora da última atualização do usuário.
    """

    user_id: str
    name: str | None = None
    email: str
    role: Optional[RoleRead] = None
    is_deleted: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_serializer("created_at", "updated_at", mode="plain")
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
        
        return value.astimezone(settings.zone_info).isoformat()
