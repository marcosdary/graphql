from fastapi import APIRouter, Response, Request, status
from json import dumps

from app.config import settings
from app.utils import decode_sign_token

router = APIRouter(prefix="/webhook", tags=["Webhook"])

@router.post(
    "",
)
async def webhook(response: Response, request: Request) -> dict:
    headers: dict = request.headers
    x_webhook_secret = headers.get("x-webhook-secret") 

    if not x_webhook_secret == settings.WEBHOOK_SECRET:
        response.status_code = status.HTTP_409_CONFLICT
        return {}

    data: dict = await request.json()
    value = data.get("data")

    if not value:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {}
    try: 
        decoded = decode_sign_token(key=settings.WEBHOOK_SECRET, value=value)
        print(decoded)
    except Exception: 
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {}

    response.status_code = status.HTTP_204_NO_CONTENT
    return {}