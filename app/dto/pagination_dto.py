from pydantic import BaseModel

class PaginationSchema(BaseModel):
    page: int | None = None
    limit: int | None = None
    all_: bool | None = False