import re
from pydantic import field_validator

from app.dto.user.model import UserModel
from app.exceptions import InvalidFieldsException


class UserLoginModel(UserModel):
    """
    Modelo de dados utilizado para autenticação de usuários.

    Esta classe estende UserModel e adiciona validações específicas
    para o processo de login, como validação do formato de e-mail.

    Attributes:
        email (str): Endereço de e-mail do usuário.
        password (str | None): Senha do usuário. Pode ser None caso não fornecida.
    """

    email: str
    password: str | None = None

    @field_validator("email", mode="after")
    def validate_email(cls, email) -> str:
        """
        Valida se o e-mail fornecido está no formato correto.

        Args:
            email (str): Endereço de e-mail fornecido pelo usuário.

        Returns:
            str: E-mail validado.

        Raises:
            InvalidFieldsException: Caso o e-mail esteja em formato inválido.
        """
        
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email) is None:
            raise InvalidFieldsException(
                "Campo e-mail inválido. Faça corretamente."
            )
        return email