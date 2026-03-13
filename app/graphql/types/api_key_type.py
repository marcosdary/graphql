from strawberry.experimental.pydantic import type as pydantic_type

from app.dto.api_key import ApiKeyRead

@pydantic_type(ApiKeyRead, all_fields=True)
class ApiKeyType:
    pass
