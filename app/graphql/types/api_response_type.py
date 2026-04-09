import strawberry
from typing import TypeVar, Generic

T = TypeVar("T")
E = TypeVar("E")

@strawberry.type
class ApiResponseType(Generic[T, E]):
    success: bool
    data: T | None = None
    error: E | None = None
