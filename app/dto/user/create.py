from pydantic import field_serializer, field_validator
import re
from random import randint

from app.constants import Roles
from app.dto.user.model import UserModel
from app.services import HashPassword
from app.exceptions import InvalidFieldsException, UnprocessableEntity


class UserCreateModel(UserModel):
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
    role: str | None = Roles.USER.value

    @field_serializer("password", mode="plain")
    def serialize_password(self, value: str) -> str:
        """
        Serializa a senha do usuário aplicando hash antes da persistência.

        Args:
            value (str): Senha em texto puro fornecida pelo usuário.

        Returns:
            str: Senha criptografada utilizando o serviço de hash.
        """
        hash_password = HashPassword()
        return hash_password.hash_password(value)

    @field_validator("role", mode="after")
    def validate_role(cls, role) -> str:
        """
        Valida se o papel (role) informado existe nas opções disponíveis.

        Args:
            role (str): Papel informado para o usuário.

        Returns:
            str: Valor válido correspondente ao papel definido na enumeração Roles.

        Raises:
            UnprocessableEntity: Caso o papel informado não exista nas opções permitidas.
        """
        field = getattr(Roles, role, None)
        if not field:
            raise UnprocessableEntity(
                "Escolha uma das opções de status para o cliente 'admin' ou 'user'."
            )
        return field.value

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
