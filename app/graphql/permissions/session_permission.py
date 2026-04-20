from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError

from app.services import token
from app.exceptions import InvalidFieldsException


class SessionPermission(BasePermission):

    def __init__(self):
        super().__init__()
        self._session_service = token.SessionService()
        

    async def has_permission(self, source, info, **kwargs):
        try:
            # o token já foi validado pelo middleware, mas garantimos aqui
            # que ele esteja presente (fallback) e recuperamos o payload.
            header: dict = info.context["request"].headers
            params: dict = info.context["request"].query_params
    
            auth = header.get("Authorization")

            if not auth:
                raise InvalidFieldsException("Não possui o Session ID. Forneça para completar a ação")

            try:
                scheme, session_id = auth.split(" ")

                if scheme.lower() != "bearer":
                    return False
                
            except ValueError:
                return False
            
            response = await self._session_service.verify_session(session_id=session_id)

            if params.get("logout") == "true":
                await self._session_service.delete_session(session_id)
            
            info.context["user"] = response
        
            return True
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc), extensions={
                "typeError": exc.__class__.__name__,
                "statusCode": getattr(exc, "status_code", 500)
            })