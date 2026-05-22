from strawberry.experimental.pydantic import type as pydantic_type


from app.dto.two_factor_auth import TwoFactorAuth
@pydantic_type(TwoFactorAuth, all_fields=True)
class TwoFactorAuthType:
    pass





