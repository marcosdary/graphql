import strawberry
from datetime import datetime
from typing import TypeVar, Generic, Optional

T = TypeVar("T")
E = TypeVar("E")

@strawberry.type
class ApiResponseType(Generic[T, E]):
    success: bool
    data: Optional[T] = None
    error: Optional[E] = None
    timestamp: datetime 
