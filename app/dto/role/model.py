from pydantic import BaseModel, ConfigDict


class RoleModel(BaseModel):
    

    model_config = ConfigDict(from_attributes=True)