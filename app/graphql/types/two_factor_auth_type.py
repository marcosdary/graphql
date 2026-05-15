from strawberry.experimental.pydantic import type as pydantic_type
import strawberry

from app.dto.two_factor_auth import TwoFactorAuth
@pydantic_type(TwoFactorAuth, all_fields=True)
class TwoFactorAuthType:
    pass





