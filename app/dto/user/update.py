from pydantic import field_serializer

from app.dto.user.model import UserModel
from app.services import HashPassword


class UserUpdateModel(UserModel):
    """
    Modelo de dados utilizado para atualização de informações de usuários.

    Esta classe estende UserModel e permite atualizar campos opcionais
    como nome, e-mail e senha. A senha, se fornecida, será automaticamente
    serializada (hash) antes de ser persistida.

    Attributes:
        name (str | None): Novo nome do usuário. Pode ser None se não for alterado.
        email (str | None): Novo e-mail do usuário. Pode ser None se não for alterado.
        password (str | None): Nova senha do usuário. Se None, a senha não será alterada.
    """

    name: str | None = None
    email: str | None = None
    password: str | None = None

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
            hash_password = HashPassword()
            return hash_password.hash_password(value)
        return value