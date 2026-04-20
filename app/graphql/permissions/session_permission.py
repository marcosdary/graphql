from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError

from app.services import token, rate_limit
from app.constants import RolePermissions
from app.exceptions import InvalidFieldsException, ProtectedRouteError

async def check_session_permission(session_id: str, field_name: str) -> dict:
    session_service = token.SessionService()

    data: dict = await session_service.verify_session(session_id=session_id)

    role = data.get("role")

    verify_field = getattr(RolePermissions, role)
    
    if not verify_field.has_permissions(field_name):
        raise ProtectedRouteError("Forneça as credenciais corretas para acessar as informações.")
    
    return data

class SessionPermission(BasePermission):

    def __init__(self):
        super().__init__()
        self._check_limit = rate_limit.check_rate_limit
        self._session_service = token.SessionService()
        

    async def has_permission(self, source, info, **kwargs):
        try:
            # o token já foi validado pelo middleware, mas garantimos aqui
            # que ele esteja presente (fallback) e recuperamos o payload.
            header: dict = info.context["request"].headers
            params: dict = info.context["request"].query_params
            client = info.context["request"].client
            field_name = info._raw_info.field_name
            auth = header.get("Authorization")

            if not auth:
                raise InvalidFieldsException("Não possui o Session ID. Forneça para completar a ação")

            # self._check_limit(client.host)

            try:
                scheme, token = auth.split(" ")

                if scheme.lower() != "bearer":
                    return False
                
            except ValueError:
                return False
            
            response = await check_session_permission(token, field_name=field_name)

            if params.get("logout") == "true":
                await self._session_service.delete_session(token)

            info.context["user"] = response
        
            return True
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc), extensions={
                "typeError": exc.__class__.__name__,
                "statusCode": getattr(exc, "status_code", 500)
            })