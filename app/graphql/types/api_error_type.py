from strawberry.experimental.pydantic import type as pydantic_type

from app.dto.api_error import ApiErrorModel

@pydantic_type(ApiErrorModel, all_fields=True)
class ApiErrorType:
    pass
