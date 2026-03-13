from strawberry.experimental.pydantic import type as pydantic_type
import strawberry

from app.dto import two_factor_auth

@pydantic_type(two_factor_auth.TwoFactorAuthModel)
class TwoFactorAuthType:
    token: strawberry.auto
    expiresAt: strawberry.auto
