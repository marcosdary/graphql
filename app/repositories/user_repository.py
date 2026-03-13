from sqlalchemy.exc import IntegrityError

from app.models import User
from app.dto.user import (
    UserCreateModel,
    UserReadModel,
    UserUpdateModel,
    UserLoginModel
)

from app.constants import Session
from app.exceptions import (
    DuplicateReviewError,
    NotFoundError,
    EntityValidationError,
    InvalidCredentialsException,
    ForbiddenActionError
)

from app.services import HashPassword

class UserRepository:
    def create_user(self, create_user: UserCreateModel) -> UserReadModel:
        with Session() as session:
            email_exists = session.query(User).filter_by(email=create_user.email).first()
            if email_exists:
                raise DuplicateReviewError("Email está em uso.")

            if create_user.role == "SUPER_ADMIN":
                raise DuplicateReviewError("Registro de Administrador negado, pois só pode ter um único master.")

            new_user = User(**create_user.model_dump())
            session.add(new_user)
            try:
                session.commit()
                return UserReadModel.model_validate(new_user)
            
            except IntegrityError:
                session.rollback()
                raise EntityValidationError("Não foi possível criar o usuário.")
            
            except Exception as exc:
                session.rollback()
                raise exc
            

    def get_user_by_email_and_password(self, login: UserLoginModel) -> UserReadModel:
        with Session() as session:
            user = session.query(User).filter_by(
                email=login.email
            ).first()
            if not user:
                raise InvalidCredentialsException("E-mail ou senha inválidos ou não cadastrados.")
            
            if not HashPassword().verify_password(login.password, user.password):
                raise InvalidCredentialsException("Senha inválida ou incorreta.")
            
            return UserReadModel.model_validate(user)
        
    
    def get_user_by_email(self, login: UserLoginModel) -> UserReadModel:
        with Session() as session:
            user = session.query(User).filter_by(
                email=login.email
            ).first()
            if not user:
                raise InvalidCredentialsException("E-mail ou senha inválidos ou não cadastrados.")
    
            return UserReadModel.model_validate(user)
        

    def update_user(self, userId: str, user_update: UserUpdateModel) -> UserReadModel:
        with Session() as session:
            user = session.query(User).filter(User.userId == userId).first()
            if not user:
                raise NotFoundError("Usuário não encontrado.")

            for key, value in user_update.model_dump().items():
                if value is not None:
                    setattr(user, key, value)

            try:
                session.commit()
                return UserReadModel.model_validate(user)
            
            except IntegrityError:
                session.rollback()
                raise EntityValidationError("Não foi possível atualizar o usuário.")
            except Exception as exc:
                session.rollback()
                raise exc
            

    def get_user_by_id(self, user_id: str) -> UserReadModel :
        with Session() as session:
            user = session.query(User).filter(User.userId == user_id).first()
            if not user:
                raise NotFoundError("Usuário não encontrado.")
            return UserReadModel.model_validate(user)
        
        
    def list_users(self) -> list[UserReadModel]:
        with Session() as session:
            users = session.query(User).all()
            return [
                UserReadModel.model_validate(u)
                for u in users
            ]


    def delete_user(self, user_id: str) -> None:
        with Session() as session:
            user = session.query(User).filter(User.userId == user_id).first()

            if not user:
                raise NotFoundError("Usuário não encontrado.")

            if user.role == "SUPER_ADMIN":
                raise ForbiddenActionError("Não pode apagar o admin do sistema. Ação inválida. Acione o suporte para esclarecimento.")
            try:
                session.delete(user)
                session.commit()
            except Exception as exc:
                session.rollback()
                raise exc
