from typing import Optional
from app.dto.user.model import UserModel

class UserCreateDB(UserModel): 
    name: str
    email: str
    password: str 
    role_id: str
