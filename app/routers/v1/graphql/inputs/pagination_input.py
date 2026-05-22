from strawberry.experimental.pydantic import input as pydantic_input

from app.dto.pagination import Pagination

@pydantic_input(Pagination, all_fields=True)
class PaginationInput:
    pass

