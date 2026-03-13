from strawberry.experimental.pydantic import type as pydantic_type
import strawberry

from app.dto.password_reset import PasswordResetModel

@pydantic_type(PasswordResetModel)
class PasswordResetType:
    token: strawberry.auto
    message: strawberry.auto
    expiresAt: strawberry.auto

