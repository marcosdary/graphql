from app.dto.api_error import ApiErrorModel
from app.graphql.base_type import ApiResponse
from app.constants import ExpirationTimes
from app.services import token, Email
from app.template import Template


def build_response(success: bool, data=None, exc: Exception | None = None) -> ApiResponse:
    """Constrói um ApiResponse padronizado.

    Args:
        success: Indica se a operação foi bem‑sucedida.
        data: Valor a ser retornado quando success=True.
        exc: Exceção capturada quando success=False.

    Returns:
        ApiResponse: objeto pronto para ser retornado ao cliente.
    """
    if success:
        return ApiResponse(success=True, data=data)

    # Caso de erro
    return ApiResponse(
        success=False,
        error=ApiErrorModel(
            typeError=exc.__class__.__name__ if exc else "Error",
            errorName=str(exc) if exc else "",
            statusCode=getattr(exc, "status_code", 500),
        ),
    )


def create_session(userId: str, role: str):
    session_service = token.SessionService()
    return session_service.create_session(
        userId=userId, 
        role=role, 
        expiration=ExpirationTimes.SESSION_EXPIRATION.value
    )

def send_email(subject: str, to_email: str, template: Template): 
    email = Email(to_email)
    email.send(subject=subject, body=template.get_template)    
