from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse

from app.services.token import ApiKeyService

class ApiKeyMidlleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        request.state.api_key = None

        token = request.headers.get("x-api-key")

        if token:
            try:
                api_key_service = ApiKeyService()
                await api_key_service.check_api_key(token)
                request.state.api_key = token
            except Exception as exc:
                return JSONResponse(
                    status_code=getattr(exc, "status_code", 401),
                    content={"detail": str(exc)},
                )

        return await call_next(request)