from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from httpx import AsyncClient

from app.core.config import settings, get_session
from app.dto.user import UserGoogle, UserCreateDB, UserCreate
from app.repositories import UserRepository
from app.exceptions import NotFoundError

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
async def callback(code: str, session: AsyncSession =  Depends(get_session)):
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

    user_google = UserGoogle.model_validate(data)
    user_repo = UserRepository(session)
    try: 
        user = user_repo.get_user_by_id(schema.sub)
    except NotFoundError as exc:
        data = UserCreate(
            name=user_google.name,
            email=user_google.email,
            google_id=user_google.sub
        )
        schema = UserCreateDB(
            name=schema.name,
            email=schema.email,
            google_id=schema.sub,
            password=schema.password
        )
        user = user_repo.create_user(schema)
        
    return user