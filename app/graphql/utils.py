from datetime import datetime
from fastapi import Request, Response

from app.dto.api_error import ApiErrorModel
from app.graphql.types import ApiResponseType
from app.constants import SendType, ExpirationAt
from app.services import token, queries
from app.dto.notification_system import (
    NotificationSystemCreateModel
)


def build_response(success: bool, data=None, exc: Exception | None = None) -> ApiResponseType:
    """Constrói um ApiResponseType padronizado.

    Args:
        success: Indica se a operação foi bem‑sucedida.
        data: Valor a ser retornado quando success=True.
        exc: Exceção capturada quando success=False.

    Returns:
        ApiResponseType: objeto pronto para ser retornado ao cliente.
    """
    if success:
        return ApiResponseType(
            success=True, 
            data=data, 
            timestamp=datetime.now().timestamp()
        )

    # Caso de erro
    return ApiResponseType(
        success=False,
        error=ApiErrorModel(
            typeError=exc.__class__.__name__ if exc else "Error",
            errorName=str(exc) if exc else "",
            statusCode=getattr(exc, "status_code", 500),
        ),
        timestamp=datetime.now().timestamp()
    )


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
