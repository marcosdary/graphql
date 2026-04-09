from datetime import datetime

from app.dto.notification_system.model import NotificationSystemModel

class NotificationSystemReadModel(NotificationSystemModel):
    idEmail: str
    status: str 
    providerResponse: str | None = None
    createdAt: datetime | None = None
    processedAt: datetime | None = None