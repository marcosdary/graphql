from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_
from typing import List
from datetime import datetime, time, timedelta
from fastapi.concurrency import run_in_threadpool

# Model
from app.models import User

# DTOs
from app.dto.user import (
    UserCreateDB,
    UserUpdateDB,
    UserLogin,
    FilterBy
)
from app.dto.pagination import Pagination

# Core
from app.core.config import Auth
from app.core.constants import Roles

# Exceptions
from app.exceptions import (
    DuplicateReviewError,
    NotFoundError,
    InvalidCredentialsException,
    ForbiddenActionError
)


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_user(self, create_user: UserCreateDB) -> User:
        
        query = await self.session.execute(
            select(User.email).where(User.email == create_user.email)
        )

        email_exists = query.first()

        if email_exists:
            raise DuplicateReviewError("Email está em uso.")
        
        user = User(**create_user.model_dump())

        self.session.add(user)

        await self.session.flush()
        return user

    async def get_user_by_email_and_password(self, login: UserLogin) -> User:
        
        query = await self.session.execute(
            select(User.user_id, User.email, User.password, User.role_id).where(User.email == login.email)
        )

        user = query.first()
            
        if not user:
            raise InvalidCredentialsException(
                "E-mail ou senha inválidos. " \
                "Em dúvida, entre em contato com suporte."
            )
         
        is_valid = await run_in_threadpool(
            Auth().verify_password,
            login.password, 
            user.password
        )

        if not is_valid:
            raise InvalidCredentialsException("E-mail ou senha inválidos..")   
        return user
    

    async def get_user_by_email(self, login: UserLogin) -> User:
       
        user = await self.session.scalar(
            select(User).where(
                User.email==login.email, 
                User.is_deleted != True
            )
        )
            
        if not user:
            raise InvalidCredentialsException("E-mail ou senha inválidos ou não cadastrados ou apagados.")
    
        return user 


    async def update_user(self, user_update: UserUpdateDB) -> User:
        user = await self.session.scalar(
            select(User).where(
                User.user_id==user_update.user_id, 
                User.is_deleted != True
            )
        )
                    
        if not user:
            raise NotFoundError("Usuário não encontrado ou removido do sistema.")
       
        for key, value in user_update.model_dump().items():
            if value is not None:
                setattr(user, key, value)
            
        return user
            

    async def get_user_by_id(self, id: str, is_google: bool = False) -> User:
        query = select(User).where(User.user_id == id)

        if is_google:
            query = select(User).where(User.google_id == id)

        user = await self.session.scalar(
            query
        )
            
        if not user:
            raise NotFoundError("Usuário não encontrado.")

        return user
        
        
    async def list_users(self, pagination: Pagination, filter_by: FilterBy = None) -> List[User]:
       
        query = select(
            User
        )

        filters = self.__filters_by(filter_by=filter_by)
            
        page, limit = 1, 10
            
        if not pagination.all_:
            if pagination.page and pagination.limit:
                page, limit = pagination.page, pagination.limit
            
        offset = (page - 1) * limit

        list_query = query.order_by(User.created_at.desc()).offset(offset).limit(limit)

        if filters:
            list_query = list_query.where(and_(*filters))
            
        stmt = await self.session.scalars(
            list_query
        )

        rows = stmt
            
        return rows


    async def delete_user(self, user_id: str) -> None:
        
        user = await self.session.scalar(
            select(User).where(User.user_id == user_id)
        )

        if not user:
            raise NotFoundError("Usuário não encontrado.")

        if user.role.name == Roles.super_admin.value:
            raise ForbiddenActionError(
                "Ação não permitida. " \
                "Por favor, entre em contato com o suporte"
            )

        await self.session.delete(user)


    async def delete_inactive_users(self) -> None:
       
        try:
            await self.session.execute(
                delete(User).where(User.is_deleted == True)
            )
            await self.session.commit()
            return

        except SQLAlchemyError as exc:
            await self.session.rollback()
            raise exc
            
    # Others methods for count rows
    def __filters_by(self, filter_by: FilterBy = None) -> List[bool]:
        filters = []

        if not filter_by:
            return filters
        
        if filter_by.name:
            name = filter_by.name.strip()
            filters.append(
                User.name.ilike(f"%{name}%")
            )

        if filter_by.is_deleted is not None:
            filters.append(
                User.is_deleted == filter_by.is_deleted
            )
    
        if filter_by.created_at:
            start = datetime.combine(filter_by.created_at, time.min)
            end = start + timedelta(days=1)
            filters.append(
                User.created_at >= start
            )
            filters.append(
                User.created_at < end
            )
        
        return filters
