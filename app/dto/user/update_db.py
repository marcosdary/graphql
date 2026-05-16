from typing import Optional

# DTOs 
from app.dto.user.model import UserModel


class UserUpdateDB(UserModel):
    user_id: str 
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None 
    role_id: Optional[str] = None

