from jwt.exceptions import InvalidSignatureError

from app.services.token.base import BaseService
from app.dto.session import Session
from app.core.config import settings

from app.exceptions import SessionError

class SessionService(BaseService):
    def __init__(self):
        self._session_key = settings.SESSION_KEY
        super().__init__()

    def create_session(self, **kwargs) -> Session:     
        token = self._encode(kwargs, self._session_key)
        return Session(
            session_id=token
        )

    def verify_session(self, session_id: str) -> dict:
        try: 
            return self._decode(session_id, self._session_key)
        except InvalidSignatureError:
            raise SessionError("Erro relacionado à sessão do usuário ou ao gerenciamento de sessão.")