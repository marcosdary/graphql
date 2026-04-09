from sqlalchemy import Column, String, Boolean, Enum
from uuid import uuid4

from app.models.base_model import Base
from app.constants import Roles
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

    userId = Column(String(255), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(255), nullable=False)
    role = Column(Enum(Roles), nullable=False, default="USER")
    email = Column(String(255), nullable=False, unique=True)
    isDeleted = Column(Boolean, default=False)
    password = Column(String(255), nullable=False)
