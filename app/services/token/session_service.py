from datetime import datetime, timedelta
from typing import Tuple

from app.services.token.base import BaseService
from app.dto.session import SessionModel
from app.config import settings
from app.constants import ExpirationTimes
from app.exceptions import SessionError

class SessionService(BaseService):
    def __init__(self):
        self._session_key = settings.SESSION_KEY
        self._session_expiration = ExpirationTimes.SESSION_EXPIRATION.value
        super().__init__()

    def __get_expiration(self) -> Tuple[datetime]:
        now = datetime.now()
        return now, now + timedelta(seconds=self._session_expiration)

    async def create_session(self, **kwargs) -> SessionModel:     
        now, expires_at = self.__get_expiration()
        
        token = self._encode(kwargs, self._session_key)
        await self._store_with_expiration(token, kwargs.get("userId"), self._session_expiration)

        return SessionModel(
            sessionId=token,
            createdAt=now,
            expiresAt=expires_at
        )

    async def verify_session(self, session_id: str) -> dict:
        data = await self._fetch_or_none(session_id)
        
        if data is None:
            raise SessionError("Sessão inválida ou expirada.")

        return self._decode(session_id, self._session_key)

    async def delete_session(self, session_id: str) -> None:
        await self._delete(session_id)