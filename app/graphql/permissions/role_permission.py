from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError

from app.core.constants import Roles
from app.exceptions import ProtectedRouteError

async def check_roles(role: str) -> None:
    
    if Roles.user.value == role:
        raise ProtectedRouteError("Forneça as credenciais corretas para acessar as informações.")
    
    return 

class RolePermission(BasePermission):

    async def has_permission(self, source, info, **kwargs):
        try:
            role = info.context.role
            await check_roles(role)
        
            return True
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc))