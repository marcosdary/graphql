from strawberry.experimental.pydantic import input as pydantic_input

from app.dto.api_key import (
    ApiKeyCreate
)

@pydantic_input(ApiKeyCreate, all_fields=True)
class ApiKeyInput:
    pass
