from strawberry.experimental.pydantic import type as pydantic_type
import strawberry

from app.dto.two_factor_auth import TwoFactorAuthModel
@pydantic_type(TwoFactorAuthModel, all_fields=True)
class TwoFactorAuthType:
    pass





