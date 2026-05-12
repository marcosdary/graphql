from pydantic import BaseModel
class ApiKeyRead(BaseModel):
    token: str
    