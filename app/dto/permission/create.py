from pydantic import BaseModel

class PermissionCreate(BaseModel):
    name: str