from strawberry.experimental.pydantic import input as pydantic_input
import strawberry

from app.dto.user import (
    UserCreateModel,
    UserUpdateModel,
    UserLoginModel,
    UserResetPasswordModel
)
from app.dto.two_factor_auth import TwoFactorAuthModel
from app.dto.password_reset import PasswordResetModel

# Criação de usuário comum
@pydantic_input(UserCreateModel)
class UserInput:
    name: strawberry.auto 
    email: strawberry.auto
    password: strawberry.auto

# Criação de usuário (admin)
@pydantic_input(UserCreateModel)
class UserPrivateInput:
    name: strawberry.auto
    email: strawberry.auto
    role: strawberry.auto

# Atualização de suas informações
@pydantic_input(UserUpdateModel)
class UserUpdateInput:
    name: strawberry.auto 

# Login
@pydantic_input(UserLoginModel, all_fields=True)
class UserLoginInput:
    pass

# Verifição de dois fatores
@pydantic_input(TwoFactorAuthModel)
class Verify2FAInput:
    number: strawberry.auto
    token: strawberry.auto

# Realizar a renovação da senha

# Pedido de recuperação
@pydantic_input(UserLoginModel)
class ForgotPasswordInput:
    email: strawberry.auto

# Verificação de código e número
@pydantic_input(PasswordResetModel)
class VerifyCodeInput:
    token: str
    number: int

# Redefinir nova senha
@pydantic_input(UserResetPasswordModel, all_fields=True)
class UserResetPasswordInput:
    pass


