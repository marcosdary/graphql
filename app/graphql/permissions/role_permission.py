from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError

from app.constants import RolePermissions
from app.exceptions import ProtectedRouteError

async def check_roles(role: str, field_name: str) -> None:

    verify_field = getattr(RolePermissions, role)
    
    if not verify_field.has_permissions(field_name):
        raise ProtectedRouteError("Forneça as credenciais corretas para acessar as informações.")
    
    return 

class RolePermission(BasePermission):

    async def has_permission(self, source, info, **kwargs):
        try:
        
            field_name = info._raw_info.field_name
            
            context: dict = info.context["user"]
            *_, role = context.values()
    
            await check_roles(role, field_name=field_name)
        
            return True
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc), extensions={
                "typeError": exc.__class__.__name__,
                "statusCode": getattr(exc, "status_code", 500)
            })