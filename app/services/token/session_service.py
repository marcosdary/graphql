from app.services.token.base import BaseService
from app.dto.session import SessionModel
from app.core.config import settings

from app.exceptions import SessionError

class SessionService(BaseService):
    def __init__(self):
        self._session_key = settings.SESSION_KEY
        super().__init__()

    async def create_session(self, **kwargs) -> SessionModel:     
        token = self._encode(kwargs, self._session_key)
        return SessionModel(
            sessionId=token
        )

    async def verify_session(self, session_id: str) -> dict:
        data = await self._fetch_or_none(session_id)
        
        if data is None:
            raise SessionError("Sessão inválida ou expirada.")

        return self._decode(session_id, self._session_key)
