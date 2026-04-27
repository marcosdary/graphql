from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, delete, func, and_
from typing import List
from datetime import datetime, time, timedelta
from fastapi.concurrency import run_in_threadpool

from app.models import User
from app.dto.user import (
    UserCreateModel,
    UserReadModel,
    UserUpdateModel,
    UserLoginModel,
    UserListModel,
    FilterByModel
)
from app.dto.pagination import PaginationModel

from app.config import AsyncSessionLocal as AsyncSession
from app.constants import Roles
from app.exceptions import (
    DuplicateReviewError,
    NotFoundError,
    EntityValidationError,
    InvalidCredentialsException,
    ForbiddenActionError
)

from app.services import HashPassword

class UserRepository:
    async def create_user(self, create_user: UserCreateModel) -> UserReadModel:
        async with AsyncSession() as session:
            query = await session.execute(
                select(User.email).where(User.email == create_user.email)
            )

            email_exists = query.first()

            if email_exists:
                raise DuplicateReviewError("Email está em uso.")

            if create_user.role == Roles.SUPER_ADMIN:
                raise DuplicateReviewError(
                    "Registro de Administrador negado, " \
                    "pois só pode ter um único master."
                )
            
            hashed_pw = await run_in_threadpool(
                HashPassword().hash_password, 
                create_user.password
            )
            
            user_data = (
                create_user.
                model_copy(update={"password": hashed_pw}).
                model_dump()
            )
            
            new_user = User(**user_data)

            session.add(new_user)
            try:
                await session.commit()
                return UserReadModel.model_validate(new_user)
            
            except IntegrityError:
                await session.rollback()
                raise EntityValidationError("Não foi possível criar o usuário.")
            
            except SQLAlchemyError as exc:
                await session.rollback()
                raise exc
            

    async def get_user_by_email_and_password(self, login: UserLoginModel) -> UserReadModel:
        async with AsyncSession() as session:
            query = await session.execute(
                select(User.userId, User.email, User.role, User.password).where(User.email == login.email)
            )

            user = query.first()
            
            if not user:
                raise InvalidCredentialsException(
                    "E-mail ou senha inválidos. " \
                    "Em dúvida, entre em contato com suporte."
                )
            
            is_valid = await run_in_threadpool(
                HashPassword.verify_password,
                login.password, 
                user.password
            )

            if not is_valid:
                raise InvalidCredentialsException("E-mail ou senha inválidos..")
            
            return UserReadModel.model_validate(user)
    
    async def get_user_by_email(self, login: UserLoginModel) -> UserReadModel:
        async with AsyncSession() as session:
            query = await session.execute(
                select(User.userId, User.email).where(
                    User.email==login.email, 
                    User.isDeleted != True
                )
            )
            user = query.first()
            
            if not user:
                raise InvalidCredentialsException("E-mail ou senha inválidos ou não cadastrados ou apagados.")
    
            return UserReadModel.model_validate(user)    

    async def update_user(self, user_update: UserUpdateModel) -> UserReadModel:
        async with AsyncSession() as session:

            try:
                query = await session.execute(
                    select(User).where(
                        User.userId==user_update.userId, 
                        User.isDeleted != True
                    )
                )
                user = query.scalars().first()
                
                if not user:
                    raise NotFoundError("Usuário não encontrado ou removido do sistema.")
                
                if user_update.role == Roles.SUPER_ADMIN:
                    raise DuplicateReviewError(
                        "Registro de Administrador negado, pois só pode ter um único master. " \
                        "Entre em contato com o suporte para potenciais mudanças."
                    )

                for key, value in user_update.model_dump().items():
                    if value is not None:
                        setattr(user, key, value)
                    await session.commit()
                    return UserReadModel.model_validate(user)
            
            except IntegrityError:
                await session.rollback()
                raise EntityValidationError("Não foi possível atualizar o usuário.")
            
            except SQLAlchemyError as exc:
                await session.rollback()
                raise exc
            

    async def get_user_by_id(self, user_id: str) -> UserReadModel:
        async with AsyncSession() as session:
            query = await session.execute(
                select(User).where(User.userId == user_id)
            )

            user = query.scalars().first()
            
            if not user:
                raise NotFoundError("Usuário não encontrado.")

            return UserReadModel.model_validate(user)
        
        
    async def list_users(self, pagination: PaginationModel, filter_by: FilterByModel = None) -> UserListModel:
        async with AsyncSession() as session:
           
            query = select(
                User.userId, User.name, User.email, 
                User.role, User.isDeleted, User.createdAt, 
                User.updatedAt
            )

            filters = self.__filters_by(filter_by=filter_by)
            
            page, limit = 1, 10
            
            if not pagination.all_:
                if pagination.page and pagination.limit:
                    page, limit = pagination.page, pagination.limit
            
            offset = (page - 1) * limit

            list_query = query.order_by(User.createdAt.desc()).offset(offset).limit(limit + 1)

            if filters:
                list_query = list_query.where(and_(*filters))
            
            stmt = await session.execute(
                list_query
            )
            rows = stmt.all()
            
            has_next = len(rows) > limit
            items = rows[:limit]

            return UserListModel(
                items=[UserReadModel.model_validate(u) for u in items],
                page=page,
                limit=limit,
                hasNextPage=has_next
            )


    async def delete_user(self, user_id: str) -> None:
        async with AsyncSession() as session:
            query = await session.execute(
                select(User).where(User.userId == user_id)
            )
            user = query.scalars().first()

            if not user:
                raise NotFoundError("Usuário não encontrado.")

            if user.role == Roles.SUPER_ADMIN:
                raise ForbiddenActionError(
                    "Ação não permitida. Não pode apagar o ADMIN. " \
                    "Por favor, entre em contato com o suporte"
                )

            await session.delete(user)
            try:
                await session.commit()
                return
            except SQLAlchemyError as exc:
                await session.rollback()
                raise exc

    async def delete_inactive_users(self) -> None:
        async with AsyncSession() as session:
            try:
                await session.execute(
                    delete(User).where(User.isDeleted == True)
                )
                await session.commit()
                return

            except SQLAlchemyError as exc:
                await session.rollback()
                raise exc
            
    # Others methods for count rows

    async def __count_rows(self, session, filters: List[bool] = None) -> int:
        count_query = select(func.count()).select_from(User)

        if filters:
            count_query = count_query.where(and_(*filters))

        total = await session.scalar(count_query)
        return total or 0

    def __filters_by(self, filter_by: FilterByModel = None) -> List[bool]:
        filters = []

        if not filter_by:
            return filters
        
        if filter_by.name:
            name = filter_by.name.strip()
            filters.append(
                User.name.ilike(f"%{name}%")
            )

        if filter_by.isDeleted is not None:
            filters.append(
                User.isDeleted == filter_by.isDeleted
            )

        if filter_by.role:
            filters.append(
                User.role == filter_by.role
            )

        if filter_by.createdAt:
            start = datetime.combine(filter_by.createdAt, time.min)
            end = start + timedelta(days=1)

            filters.append(
                User.createdAt >= start
            )
            filters.append(
                User.createdAt < end
            )

        return filters
