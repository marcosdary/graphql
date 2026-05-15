from typing import List
from pydantic import RootModel

from app.dto.user.read import UserRead

class UserList(RootModel[List[UserRead]]): pass