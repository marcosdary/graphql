from pydantic import field_validator, field_serializer
import re
from random import randint

from app.core.constants import Roles
from app.core.config import Auth
from app.dto.user.model import UserModel
from app.exceptions import InvalidFieldsException, UnprocessableEntity


class UserCreate(UserModel):
    """
    Modelo de dados utilizado para criação de um novo usuário.

    Esta classe estende UserModel e adiciona validações e transformações
    específicas para o processo de criação de usuários, como:

    - Geração automática de senha caso não seja informada.
    - Validação do formato do e-mail.
    - Validação do papel (role) do usuário.
    - Serialização da senha em formato criptografado.

    Attributes:
        name (str): Nome do usuário.
        email (str): Endereço de e-mail do usuário.
        password (str | None): Senha do usuário. Caso não seja informada,
            uma senha numérica aleatória será gerada automaticamente.
        role (str | None): Papel do usuário no sistema. O padrão é "user".
    """

    name: str
    email: str
    password: str | None = str(randint(100_000, 999_999))
    role: Roles | None = Roles.user

    @field_validator("email", mode="after")
    def validate_email(cls, email) -> str:
        """
        Valida o formato do endereço de e-mail informado.

        Args:
            email (str): Endereço de e-mail fornecido pelo usuário.

        Returns:
            str: O e-mail validado.

        Raises:
            InvalidFieldsException: Caso o formato do e-mail seja inválido.
        """
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email) is None:
            raise InvalidFieldsException(
                "Campo e-mail inválido. Faça corretamente."
            )
        return email
    
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
