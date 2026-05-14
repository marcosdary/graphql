from pydantic import RootModel
from typing import List

from app.dto.role.read import RoleRead
class RoleList(RootModel[List[RoleRead]]): pass