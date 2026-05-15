from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from uuid import uuid4

from app.models.base_model import Base

class User(Base):
    """Modelo de usuário para o banco de dados.

    Representa a entidade `users` com atributos essenciais como identificação,
    nome, papel, e-mail, senha e status de exclusão.

    Attributes:
        userId (str): Identificador único do usuário (UUID) gerado automaticamente.
        name (str): Nome completo do usuário. Obrigatório.
        role (Enum): Papel do usuário na aplicação. Pode ser "ADMIN", "USER" ou "SUPER_ADMIN".
            Padrão é "USER".
        email (str): E-mail único do usuário. Obrigatório e único.
        isDeleted (bool): Flag indicando se o usuário foi logicamente deletado. Padrão é False.
        password (str): Senha do usuário. Obrigatório.
    """

    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(nullable=False)
    
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    password: Mapped[str] = mapped_column(nullable=False)

    role_id: Mapped[str] = mapped_column(
        ForeignKey("role.role_id"),
        nullable=False,
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="users",
        lazy="joined"
    )
