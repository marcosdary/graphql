from fastapi import Request, Response
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from app.services import token
from app.core.constants import ExpirationTimes


def build_extensions(exc: Exception) -> dict:
    """Converte o padrão `build_response` para `GraphQLError.extensions`.

    Permissions do Strawberry retornam erro via GraphQL errors, então
    anexamos a estrutura padronizada em `extensions.response`.
    """
    return {
        "typeError": exc.__class__.__name__ if exc else "UnknownError",
        "statusCode": getattr(exc, "status_code", 500),
    }


async def create_session(userId: str, role: str):
    session_service = token.SessionService()
    sp = ZoneInfo("America/Sao_Paulo")
    exp = datetime.now(tz=sp) + timedelta(minutes=ExpirationTimes.SESSION_EXPIRATION.value)
    return await session_service.create_session(
        sub=userId, # subject, quem é o dono/assunto do token, normalmente o ID do usuário.
        exp=exp.timestamp(), # expiration time, quando o token expira.
        iat=datetime.now(tz=sp).timestamp(), # issued at, quando o token foi emitido.
        role=role, # papel do usuário,
        scope="authenticated"
    )

async def get_context(request: Request, response: Response):
    return {
        "request": request,
        "response": response,
        "api_key": getattr(request.state, "api_key", None)
    }
