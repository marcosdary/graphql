from fastapi import Depends, Request, Response
from datetime import datetime, timedelta
from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession

# Services
from app.services import token

# Repository
from app.repositories import RolePermissionsRepository

# Core
from app.core.constants import ExpirationTimes
from app.core.config import get_session, settings

# Context
from app.graphql.context import Context


async def get_permissions(session: AsyncSession, role: str) -> Tuple[str]:
    role_permi_repo = RolePermissionsRepository(session=session)
    rows = await role_permi_repo.list_permissions_by_role(role_id=role)
    resolvers = tuple(
        map(
            lambda row: row.permission.name,
            rows
        )
    )
    return resolvers

async def create_access_token(session: AsyncSession, user_id: str, role: str):
    session_service = token.SessionService()
    sp = settings.zone_info
    exp = datetime.now(tz=sp) + timedelta(minutes=ExpirationTimes.SESSION_EXPIRATION.value)

    scopes = await get_permissions(session, role) 
    print(scopes)

    return session_service.create_session(
        sub=user_id, # subject, quem é o dono/assunto do token, normalmente o ID do usuário.
        type="session",
        exp=int(exp.timestamp()), # expiration time, quando o token expira.
        iat=int(datetime.now(tz=sp).timestamp()), # issued at, quando o token foi emitido.
        scopes=scopes
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
