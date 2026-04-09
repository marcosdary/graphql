from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.constants import SendType, ExpirationAt


class NotificationSystemModel(BaseModel):
    recipientEmail: str
    sendType: SendType
    expiresAt: ExpirationAt | None = None

    model_config = ConfigDict(from_attributes=True)