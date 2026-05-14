from fastapi import Depends, Request, Response
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import token
from app.core.constants import ExpirationTimes
from app.core.config import get_session, settings
from app.graphql.context import Context


def create_access_token(user_id: str, role: str):
    session_service = token.SessionService()
    sp = settings.zone_info
    exp = datetime.now(tz=sp) + timedelta(minutes=ExpirationTimes.SESSION_EXPIRATION.value)
    return session_service.create_session(
        sub=user_id, # subject, quem é o dono/assunto do token, normalmente o ID do usuário.
        type="session",
        exp=int(exp.timestamp()), # expiration time, quando o token expira.
        iat=int(datetime.now(tz=sp).timestamp()), # issued at, quando o token foi emitido.
        role=role, # papel do usuário,
        scope="authenticated"
    )


async def get_context(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> Context:
    
    context = Context()

    context.request = request
    context.response = response
    context.api_key = request.headers.get("x-api-key")
    context.session = session

    return context
