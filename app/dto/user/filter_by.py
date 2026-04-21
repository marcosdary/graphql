from datetime import date

from app.constants import Roles
from app.dto.user.model import UserModel

class FilterByModel(UserModel):

    name: str | None = None
    createdAt: date | None = None
    isDeleted: bool | None = None
    role: Roles | None = None