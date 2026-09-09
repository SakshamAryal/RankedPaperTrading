from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from app.models.base import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped

if TYPE_CHECKING:
    from app.models.user import User

class Portfolio(Base):
    __tablename__ = "portfolio"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="portfolios")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(unique=True)
