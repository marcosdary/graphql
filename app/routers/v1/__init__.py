from fastapi import APIRouter

from app.routers.v1.routers import auth_router

router = APIRouter()

router.include_router(auth_router.router, prefix="/auth")



