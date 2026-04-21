from strawberry.experimental.pydantic import input as pydantic_input

from app.dto.pagination import PaginationModel

@pydantic_input(PaginationModel, all_fields=True)
class PaginationInput:
    pass

