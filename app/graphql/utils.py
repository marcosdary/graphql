from fastapi import Request, Response

from app.constants import SendType, ExpirationAt
from app.services import token, queries
from app.dto.notification_system import (
    NotificationSystemCreateModel
)

def build_extensions(exc: Exception) -> dict:
    """Converte o padrão `build_response` para `GraphQLError.extensions`.

    Permissions do Strawberry retornam erro via GraphQL errors, então
    anexamos a estrutura padronizada em `extensions.response`.
    """
    return {
        "typeError": exc.__class__.__name__ if exc else "UnknownError",
        "statusCode": getattr(exc, "status_code", 500),
    }


async def create_session(userId: str, role: str):
    session_service = token.SessionService()
    return await session_service.create_session(
        userId=userId, 
        role=role
    )

async def send_notification_to_email(
    recipient_email: str, 
    send_type: SendType, 
    expires_at: ExpirationAt = None,
    token: str = None, 
    code: str = None, 
    action_link: str = None
) -> None:
    notification_system_service = queries.NotificationSystemService()

    schema = NotificationSystemCreateModel(
        recipientEmail=recipient_email,
        sendType=send_type,
        actionLink=action_link,
        token=token,
        code=code,
        expiresAt=expires_at
    )

    await notification_system_service.create(schema)

async def get_context(request: Request, response: Response):
    return {
        "request": request,
        "response": response,
        "api_key": getattr(request.state, "api_key", None)
    }
