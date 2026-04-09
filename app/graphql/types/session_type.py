from strawberry.experimental.pydantic import type as pydantic_type

from app.dto.session import SessionModel

@pydantic_type(SessionModel, all_fields=True)
class SessionType:
    pass