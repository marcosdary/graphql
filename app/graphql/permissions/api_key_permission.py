from strawberry.permission import BasePermission
from strawberry.exceptions import StrawberryGraphQLError

from app.services.token import ApiKeyService

class ApiKeyPermission(BasePermission):
    message = "Rota protegida. Forneça sua API Key."
    error_extensions = {
        "code": "UNAUTHORIZED",
        "permission": "API_KEY",
        "statusCode": 401,
    }

    def __init__(self):
        self._api_key_service = ApiKeyService()
        super().__init__()

    async def has_permission(self, source, info, **kwargs) -> bool:
        api_key = info.context.get("api_key")
        if not api_key:
            # Delega ao Strawberry a resposta padronizada via `message`
            # e `error_extensions`.
            return False

        try:
            await self._api_key_service.check_api_key(api_key)
            return True
        except Exception as exc:
            raise StrawberryGraphQLError(
                str(exc),
                extensions={
                    "code": "UNAUTHORIZED",
                    "permission": "API_KEY",
                    "typeError": exc.__class__.__name__,
                    "statusCode": getattr(exc, "status_code", 401),
                },
            )

    def on_unauthorized(self) -> None:
        raise StrawberryGraphQLError(self.message, extensions=self.error_extensions)
