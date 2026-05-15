from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import field_serializer
from app.dto.permission.model import PermissionModel

class PermissionRead(PermissionModel):

    permission_id: str
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_serializer("created_at", "updated_at", mode="plain")
    def serialize_dates(self, value: datetime | None) -> str | None:
        """
        Serializa objetos datetime em strings no formato ISO 8601.

        Args:
            value (datetime | None): Data/hora a ser serializada.

        Returns:
            str | None: Data/hora convertida para string ISO 8601 ou None
                caso o valor seja None.
        """
        if value is None:
            return None
        
        return value.astimezone(ZoneInfo("America/Sao_Paulo")).isoformat()