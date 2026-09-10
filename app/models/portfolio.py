from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING
from app.models.base import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import ForeignKey, Numeric

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.stock import Stock

class Portfolio(Base):
    __tablename__ = "portfolio"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="portfolios")
    name: Mapped[str] = mapped_column(unique=True)
    cash_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=10000 )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    stocks: Mapped[list["Stock"]] = relationship()
