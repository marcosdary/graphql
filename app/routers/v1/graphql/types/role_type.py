from strawberry.experimental.pydantic import type as pydantic_type

from app.dto.role import RoleRead


@pydantic_type(RoleRead, all_fields=True)
class RoleType:
    pass
