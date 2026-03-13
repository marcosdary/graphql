from app.dto.user.model import UserModel


class UserResetPasswordModel(UserModel):
    """
    Modelo de dados utilizado para redefinição de senha de usuários.

    Esta classe estende UserModel e representa os dados necessários
    para realizar a redefinição de senha, incluindo a nova senha
    e o token de verificação.

    Attributes:
        password (str): Nova senha que será atribuída ao usuário.
        token (str): Token de verificação utilizado para autorizar
            a redefinição de senha.
    """

    password: str
    token: str