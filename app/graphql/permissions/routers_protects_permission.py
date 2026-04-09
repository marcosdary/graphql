from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError

from app.services import token
from app.constants import RolesRouters, Roles
from app.exceptions import InvalidFieldsException, ProtectedRouteError


async def check_session_permission(session_id: str, field_name: str) -> dict:

    session_service = token.SessionService()
    verify = await session_service.verify_session(session_id=session_id)

    if verify.get("role") == Roles.USER.name:
        raise ProtectedRouteError("Acesso negado. Ofereça informações para acessar ou entre em contato com o suporte.")

    role = verify.get("role")

    if role == Roles.ADMIN.name:
        if field_name not in RolesRouters.ADMIN.value:
            raise ProtectedRouteError("Forneça as credenciais corretas para acessar as informações.")

    if role == Roles.SUPER_ADMIN.name:
        if field_name not in RolesRouters.SUPER_ADMIN.value:
            raise ProtectedRouteError("Forneça as credenciais corretas para acessar as informações.")
    
    return verify


class RoutersProtectPermission(BasePermission):

    def __init__(self):
        super().__init__()
        
    async def has_permission(self, source, info, **kwargs):
        try:
            # o token já foi validado pelo middleware, mas garantimos aqui
            # que ele esteja presente (fallback) e recuperamos o payload.
            header: dict = info.context["request"].headers
            
            session_id = header.get("session-id")
            field_name = info._raw_info.field_name

            if not session_id:
                raise InvalidFieldsException("Não possui o Session ID. Forneça para completar a ação")

            response = await check_session_permission(session_id, field_name)
                
            info.context["user"] = response
        
            return True
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc), extensions={
                "typeError": exc.__class__.__name__,
                "statusCode": getattr(exc, "status_code", 500)
            })