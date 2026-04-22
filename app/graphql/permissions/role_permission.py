from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError

from app.constants import Roles
from app.exceptions import ProtectedRouteError

async def check_roles(role: str) -> None:
    
    if Roles.USER.value == role:
        raise ProtectedRouteError("Forneça as credenciais corretas para acessar as informações.")
    
    return 

class RolePermission(BasePermission):

    async def has_permission(self, source, info, **kwargs):
        try:
        
            field_name = info._raw_info.field_name
            
            context: dict = info.context["user"]
            *_, role = context.values()
    
            await check_roles(role)
        
            return True
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc), extensions={
                "typeError": exc.__class__.__name__,
                "statusCode": getattr(exc, "status_code", 500)
            })