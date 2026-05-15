from strawberry.permission import BasePermission
from graphql.pyutils import Path
from typing import List
from strawberry.exceptions import StrawberryGraphQLError
from datetime import datetime


# Services
from app.services import token

# Settings
from app.core.config import settings

# Exceptions
from app.exceptions import (
    InvalidFieldsException, 
    ExpirationError,
    ForbiddenActionError,
    ProtectedRouteError
)

def get_resolvers(path: Path, resolvers: List[str] = []) -> List[str]:
    resolvers.append(path.key)

    if not isinstance(path.prev, Path):
        return resolvers

    return get_resolvers(path.prev, resolvers)

class SessionPermission(BasePermission):

    def __init__(self):
        super().__init__()
        self._session_service = token.SessionService()
        

    async def has_permission(self, source, info, **kwargs):
        try:
            # o token já foi validado pelo middleware, mas garantimos aqui
            # que ele esteja presente (fallback) e recuperamos o payload.
            request = info.context.request
            header: dict = request.headers
            
            resolver = ":".join(key for key in sorted(get_resolvers(info.path), reverse=True))
           
            auth = header.get("Authorization")

            if not auth:
                raise InvalidFieldsException("Não possui o Session ID. Forneça para completar a ação")

            try:
                scheme, session_id = auth.split(" ")

                if scheme.lower() != "bearer":
                    return False
                
            except ValueError:
                return False
            
            response = self._session_service.verify_session(session_id=session_id)
            scopes = response.get("scopes")
            sp = settings.zone_info
            current = datetime.now(tz=sp).timestamp()

            exp = response.get("exp")
            if exp <= current:
                raise ExpirationError("Recurso ou sessão expirada")
            
            if resolver not in scopes:
                raise ProtectedRouteError("Acesso a rota protegida sem permissão adequada.")

            info.context.user_id = response.get("sub")
            info.context.role = response.get("role")
            return True
    
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc))