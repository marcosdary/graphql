from strawberry.fastapi import BaseContext
from functools import cached_property
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import Roles

class Context(BaseContext):
    api_key: str | None
    session: AsyncSession
    user_id: str | None 
    role: Roles | None 

__all__ = ["Context",]

