from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base
from app.core.constants import Papers

class Token(Base):

    __tablename__ = "token"

    token: Mapped[str] = mapped_column(primary_key=True)
    role: Mapped[Papers] = mapped_column(nullable=False)
    disabled: Mapped[bool] = mapped_column(default=False)