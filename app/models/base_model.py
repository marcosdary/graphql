from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    """Classe base abstrata para modelos SQLAlchemy.

    Fornece campos de auditoria comuns a todas as tabelas herdando desta
    classe, como data de criação e data de atualização.

    Attributes:
        createdAt (datetime): Data e hora em que o registro foi criado.
            Preenchido automaticamente com `datetime.now()` ao inserir o registro.
        updatedAt (datetime): Data e hora da última atualização do registro.
            Atualizado automaticamente com `datetime.now()` a cada modificação.
    """

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )
