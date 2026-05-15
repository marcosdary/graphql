from strawberry.experimental.pydantic import input as pydantic_input
from strawberry.experimental.pydantic import error_type as pydantic_error_type
import strawberry

from app.dto.user import (
    UserCreate,
    UserUpdate,
    UserLogin,
    UserResetPassword,
    FilterBy,
)
from app.dto.two_factor_auth import TwoFactorAuth
from app.dto.password_reset import PasswordReset

# Criação de usuário comum
@pydantic_input(UserCreate)
class UserInput:
    name: strawberry.auto 
    email: strawberry.auto
    password: strawberry.auto

# Criação de usuário (admin)
@pydantic_input(UserCreate)
class UserPrivateInput:
    name: strawberry.auto
    email: strawberry.auto
    password: strawberry.auto
    role: strawberry.auto

# Atualização de suas informações
@pydantic_input(UserUpdate)
class UserUpdatePublicInput:
    name: strawberry.auto 


# Atualização de suas informações
@pydantic_input(UserUpdate, all_fields=True)
class UserUpdatePrivateInput:
    pass

# Login
@pydantic_input(UserLogin, all_fields=True)
class UserLoginInput:
    pass

# Verifição de dois fatores
@pydantic_input(TwoFactorAuth)
class Verify2FAInput:
    number: strawberry.auto
    token: strawberry.auto

# Realizar a renovação da senha

# Pedido de recuperação
@pydantic_input(UserLogin)
class ForgotPasswordInput:
    email: strawberry.auto

# Verificação de código e número
@pydantic_input(PasswordReset)
class VerifyCodeInput:
    token: str
    number: int

# Redefinir nova senha
@pydantic_input(UserResetPassword, all_fields=True)
class UserResetPasswordInput:
    pass

# Filtrar por um determinado campo do model do usuário
@pydantic_input(FilterBy, all_fields=True)
class FilterByInput:
    pass


