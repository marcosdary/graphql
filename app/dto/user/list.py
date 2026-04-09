from typing import List

from app.dto.user.model import UserModel
from app.dto.user import UserReadModel

class UserListModel(UserModel):
    users: List[UserReadModel] | None = [] 