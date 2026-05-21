from datetime import datetime
from pydantic import field_serializer
from typing import Optional

# Base Model Pydantic
from app.dto.user.model import UserModel


class UserGoogle(UserModel):
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

    sub: str
    name: str 
    email: str