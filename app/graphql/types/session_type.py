from strawberry.experimental.pydantic import type as pydantic_type

from app.dto import session

@pydantic_type(session.SessionModel, all_fields=True)
class SessionType:
    pass