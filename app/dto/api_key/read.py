from pydantic import BaseModel, field_serializer
from datetime import datetime

class ApiKeyRead(BaseModel):
    token: str
    expiresAt: datetime

    @field_serializer("expiresAt", mode="plain")
    def serialize_dates(self, value: datetime | None) -> str | None:
        if value is None:
            return None
        return value.isoformat()
    