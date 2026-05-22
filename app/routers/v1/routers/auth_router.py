from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi.responses import RedirectResponse
from httpx import AsyncClient

# Core
from app.core.config import settings, get_session
from app.core.constants import Roles

# Utils
from app.utils.create_access_token import create_access_token

# DTOs
from app.dto.user import (
    UserGoogle, 
    UserCreateDB, 
    UserCreate,
    UserLogin
)
from app.dto.session import Session

# Repository
from app.repositories import UserRepository, RoleRepository

# Exceptions
from app.exceptions import (
    InvalidCredentialsException
)

router = APIRouter(tags=["Auth"])

@router.get("/google/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def login_google():
    url = (
        f"{settings.URL_GOOGLE_METADATA}"
        f"?client_id={settings.CLIENT_GOOGLE_ID}"
        f"&redirect_uri={settings.REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid email profile"
    )

    return RedirectResponse(url)

@router.get("/callback", response_model=Session)
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

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            raise HTTPException(
                detail="Falha ao acessar o servidor.", 
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        
        data = response.json()

        response = await client.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            headers={
                "Authorization": f"Bearer {data['access_token']}"
            }
        )

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            raise HTTPException(
                detail="Falha ao acessar o servidor.", 
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    data = response.json()

    user_google = UserGoogle.model_validate(data)

    role_repo = RoleRepository(session=session)
    user_repo = UserRepository(session=session)

    user = None
    try: 
        user = await user_repo.get_user_by_email(UserLogin(email=user_google.email))
    
    except InvalidCredentialsException:
        role_id = await role_repo.get_role_by_name(Roles.user.name)
        data = UserCreate(
            name=user_google.name,
            email=user_google.email
        )
        data = UserCreateDB(role_id=role_id, **data.model_dump(exclude=["role"]))
        user = await user_repo.create_user(data)
        await session.commit()

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            detail="Não foi possível criar o usuário.", 
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    except Exception as exc:
        await session.rollback()
        raise HTTPException(
            detail=str(exc), 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if not user:
        raise HTTPException(
            detail="Informação do usuário não encontrada. Tente novamente.", 
            status_code=status.HTTP_400_BAD_REQUEST
        )

    session_new = await create_access_token(
        session=session,
        user_id=user.user_id, 
        role=user.role_id
    )

    return session_new

        