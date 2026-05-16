# DTOs
from app.dto.user.model import UserModel

# Core
from app.core.constants import Roles


class UserUpdate(UserModel):
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
    user_id: str | None = None
    name: str | None = None
    email: str | None = None
    role: Roles | None = None
    password: str | None = None

