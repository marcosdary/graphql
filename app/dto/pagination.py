from pydantic import BaseModel

class PaginationModel(BaseModel):
    page: int | None = None
    limit: int | None = None
    all_: bool | None = False