from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse
from httpx import AsyncClient

from app.core.config import settings
from app.dto.user import UserGoogle

router = APIRouter(tags=["Auth"])

@router.get("/login/google", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def login_google():
    url = (
        f"{settings.URL_GOOGLE_METADATA}"
        f"?client_id={settings.CLIENT_GOOGLE_ID}"
        f"&redirect_uri={settings.REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid email profile"
    )

    return RedirectResponse(url)

@router.get("/callback", response_model=UserGoogle)
async def callback(code: str):
    async with AsyncClient() as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": settings.CLIENT_GOOGLE_ID,
                "client_secret": settings.CLIENT_GOOGLE_SECRET_ID,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.REDIRECT_URI,
            },
        )

        data = response.json()

        response = await client.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            headers={
                "Authorization": f"Bearer {data['access_token']}"
            }
        )
        
    data = response.json()

    user = UserGoogle.model_validate(data)
        
    return user