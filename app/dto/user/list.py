from typing import List

from app.dto.user.model import UserModel
from app.dto.user import UserReadModel

class UserListModel(UserModel):
    items: List[UserReadModel] | None = [] 
    total: int | None = 0
    page: int | None = 0
    limit: int | None = 0
    hasNextPage: bool | None = False
