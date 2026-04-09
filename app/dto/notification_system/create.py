from pydantic import BaseModel, field_validator, field_serializer
from datetime import datetime, timedelta
from enum import Enum

from app.constants import SendType, ExpirationAt
from app.dto.notification_system.model import NotificationSystemModel

class NotificationSystemCreateModel(NotificationSystemModel):
    actionLink: str | None = None
    code: str | None = None
    token: str | None = None


    @field_serializer("sendType", "expiresAt", mode="plain")
    def serialize_enum(self, value: Enum) -> str | int:
        return value.value if value else None
