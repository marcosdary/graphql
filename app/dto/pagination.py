from pydantic import BaseModel

class Pagination(BaseModel):
    page: int | None = None
    limit: int | None = None
    all_: bool | None = False