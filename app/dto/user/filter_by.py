from datetime import date

from app.core.constants import Roles
from app.dto.user.model import UserModel

class FilterBy(UserModel):

    name: str | None = None
    created_at: date | None = None
    is_deleted: bool | None = None
