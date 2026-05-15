from pydantic import RootModel
from typing import List

from app.dto.role_permissions.read import RolePermissionsRead

class RolePermissionsList(RootModel[List[RolePermissionsRead]]): pass