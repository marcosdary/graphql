from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4
from typing import List

from app.models.base_model import Base

class Role(Base):

    __tablename__ = "role"

    role_id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(nullable=False)

    role_permissions: Mapped[List["RolePermissions"]] = relationship(
        "RolePermissions",
        back_populates="role",
        cascade="all, delete-orphan",
    )

    users: Mapped[List["User"]] = relationship(
        "User",
        back_populates="role"
    )