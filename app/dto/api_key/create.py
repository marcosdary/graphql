from pydantic import BaseModel

from app.constants import ExpirationApiKey

class ApiKeyCreate(BaseModel):
    expiration: ExpirationApiKey