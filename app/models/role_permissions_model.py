from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from uuid import uuid4

from app.models.base_model import Base

class RolePermissions(Base):

    __tablename__ = "role_permissions"

    role_id: Mapped[str] = mapped_column(
        ForeignKey("role.role_id", ondelete="CASCADE"), 
        primary_key=True
    )
    permission_id: Mapped[str] = mapped_column(
        ForeignKey(
            "permission.permission_id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="role_permissions",
    )

    permission: Mapped["Permission"] = relationship(
        "Permission",
        back_populates="role_permissions",
    )


