from datetime import datetime, timedelta

from app.services.token.base import BaseService
from app.dto.session import SessionModel
from app.constants import settings
from app.exceptions import SessionError

class SessionService(BaseService):
    def __init__(self):
        self._session_key = settings.SESSION_KEY
        super().__init__()

    def create_session(self, expiration: int = 3600, **kwargs) -> SessionModel:
        token = self._encode(kwargs, self._session_key)
        self._store_with_expiration(token, kwargs.get("userId"), expiration)

        now = datetime.now()
        return SessionModel(
            sessionId=token,
            createdAt=now,
            expiresAt=now + timedelta(seconds=expiration)
        )

    def verify_session(self, session_id: str) -> dict:
        data = self._get_or_none(session_id)
        
        if data is None:
            raise SessionError("Sessão inválida ou expirada.")

        return self._decode(session_id, self._session_key)

    def delete_session(self, session_id: str) -> None:
        self._delete(session_id)