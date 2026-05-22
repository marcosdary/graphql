from fastapi import Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_session

# Context
from app.routers.v1.graphql.context import Context

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
