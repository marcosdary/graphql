from pydantic import RootModel
from typing import List

from app.dto.permission.read import PermissionRead

class PermissionList(RootModel[List[PermissionRead]]): pass