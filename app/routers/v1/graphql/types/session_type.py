from strawberry.experimental.pydantic import type as pydantic_type

from app.dto.session import Session

@pydantic_type(Session, all_fields=True)
class SessionType:
    pass