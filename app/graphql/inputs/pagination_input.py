from strawberry.experimental.pydantic import input as pydantic_input

from app.dto.pagination_dto import PaginationSchema

@pydantic_input(PaginationSchema, all_fields=True)
class PaginationInput:
    pass

