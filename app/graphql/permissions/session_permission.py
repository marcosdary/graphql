from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError

from app.services import token, rate_limit
from app.exceptions import InvalidFieldsException, ProtectedRouteError

ROUTERS_PROTECTS = (
    "listUsers",
    "createAdmin",
    "getAllPosts",
    "createApiKey"
)

ROUTERS_FOR_SUPER_ADMIN = (
    "createApiKey",
    "createAdmin",
)

ROLES_ADMIN = (
    "ADMIN",
    "SUPER_ADMIN"
)

def check_session_permission(session_id: str, field_name: str) -> dict:

    session_service = token.SessionService()
    verify = session_service.verify_session(session_id=session_id)

    if verify.get("role") not in ROLES_ADMIN and field_name in ROUTERS_PROTECTS:
        raise ProtectedRouteError("Rota Protegida. Forneça as credenciais corretas para acessar as informações.")

    if field_name in ROUTERS_FOR_SUPER_ADMIN and verify.get("role") != "SUPER_ADMIN":
        raise ProtectedRouteError("Forneça as credenciais corretas para acessar as informações.")
    
    return verify

class SessionPermission(BasePermission):

    def __init__(self):
        super().__init__()
        self._check_limit = rate_limit.check_rate_limit
        self._session_service = token.SessionService()
        

    def has_permission(self, source, info, **kwargs):
        try:
            # o token já foi validado pelo middleware, mas garantimos aqui
            # que ele esteja presente (fallback) e recuperamos o payload.
            header: dict = info.context["request"].headers
            params: dict = info.context["request"].query_params
            client = info.context["request"].client
            session_id = header.get("session-id")
            field_name = info._raw_info.field_name

            if not session_id:
                raise InvalidFieldsException("Não possui o Session ID. Forneça para completar a ação")

            response = check_session_permission(session_id, field_name)

            self._check_limit(client.host)

            if params.get("logout") == "true":
                self._session_service.delete_session(session_id)

            info.context["user"] = response
        
            return True
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc), extensions={
                "typeError": exc.__class__.__name__,
                "statusCode": getattr(exc, "status_code", 500)
            })