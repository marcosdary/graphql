from fastapi import Depends, Request, Response
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import token
from app.core.constants import ExpirationTimes
from app.core.config import get_session


def create_access_token(userId: str, role: str):
    session_service = token.SessionService()
    sp = ZoneInfo("America/Sao_Paulo")
    exp = datetime.now(tz=sp) + timedelta(minutes=ExpirationTimes.SESSION_EXPIRATION.value)
    return session_service.create_session(
        sub=userId, # subject, quem é o dono/assunto do token, normalmente o ID do usuário.
        exp=exp.timestamp(), # expiration time, quando o token expira.
        iat=datetime.now(tz=sp).timestamp(), # issued at, quando o token foi emitido.
        role=role, # papel do usuário,
        scope="authenticated"
    )


async def get_context(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    return {
        "request": request,
        "response": response,
        "api_key": getattr(request.state, "api_key", None),
        "session": session,
    }
