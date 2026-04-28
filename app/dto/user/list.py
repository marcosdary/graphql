from typing import List
from pydantic import RootModel

from app.dto.user import UserReadModel

class UserListModel(RootModel[List[UserReadModel]]): pass