from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.services.token import ApiKeyService

class ApiKeyMidlleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        request.state.api_key = None

        token = request.headers.get("x-api-key")
            
        request.state.api_key = token      
        
        return await call_next(request)