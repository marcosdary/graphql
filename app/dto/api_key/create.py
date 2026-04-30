from pydantic import BaseModel

from app.core.constants import ExpirationApiKey

class ApiKeyCreate(BaseModel):
    expiration: ExpirationApiKey