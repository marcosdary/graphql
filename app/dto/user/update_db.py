from pydantic import field_serializer

from typing import Optional

# DTOs 
from app.dto.user.model import UserModel

# Core
from app.core.config import Auth

class UserUpdateDB(UserModel):
    user_id: str 
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None 
    role_id: Optional[str] = None


    @field_serializer("password", mode="plain")
    def serialize_password(self, value: str) -> str:
        """
        Serializa a senha fornecida aplicando hash antes da persistência.

        Esta função só aplica o hash se a senha for fornecida.
        Caso seja None ou string vazia, retorna o valor sem alterações.

        Args:
            value (str): Senha em texto puro fornecida pelo usuário.

        Returns:
            str: Senha criptografada ou o valor original se não houver senha.
        """
        if value:
            return Auth.hash_password(value)
        return value