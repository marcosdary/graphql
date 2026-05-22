from strawberry.experimental.pydantic import type as pydantic_type
import strawberry

from app.dto.password_reset import PasswordReset

@pydantic_type(PasswordReset)
class PasswordResetType:
    token: strawberry.auto
    expires_at: strawberry.auto

