from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, delete
from fastapi.concurrency import run_in_threadpool

from app.models import User
from app.dto.user import (
    UserCreateModel,
    UserReadModel,
    UserUpdateModel,
    UserLoginModel,
    UserListModel
)

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

            user_data = create_user.model_dump()
            user_data["password"] = hashed_pw
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
                    "E-mail ou senha inválidos ou não cadastrados ou apagados. " \
                    "Em dúvida, entre em contato com suporte."
                )
            
            is_valid = await run_in_threadpool(
                HashPassword.verify_password,
                login.password, 
                user.password
            )

            if not is_valid:
                raise InvalidCredentialsException("Senha inválida ou incorreta.")
            
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

    async def update_user(self, userId: str, user_update: UserUpdateModel) -> UserReadModel:
        async with AsyncSession() as session:
            query = await session.execute(
                select(User).where(
                    User.userId==userId, 
                    User.isDeleted != True
                )
            )
            user = query.scalars().first()
            
            if not user:
                raise NotFoundError("Usuário não encontrado.")
            
            if user_update.role == Roles.SUPER_ADMIN:
                raise DuplicateReviewError(
                    "Registro de Administrador negado, pois só pode ter um único master. " \
                    "Entre em contato com o suporte para potenciais mudanças."
                )

            for key, value in user_update.model_dump().items():
                if value is not None:
                    setattr(user, key, value)

            try:
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
        
        
    async def list_users(self, page: int = 1, limit: int = 10) -> UserListModel:
        async with AsyncSession() as session:
            offset = (page - 1) * limit
            query = await session.execute(
                select(
                    User.userId, User.name, User.email, 
                    User.role, User.isDeleted, User.createdAt, 
                    User.updatedAt
                ).offset(offset).limit(limit).order_by(User.createdAt)
            )
            users = query.all()

            return UserListModel(
                users=[UserReadModel.model_validate(u) for u in users]
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

            user.isDeleted = True
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

