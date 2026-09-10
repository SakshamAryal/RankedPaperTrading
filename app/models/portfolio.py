from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING
from app.models.base import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import ForeignKey, Numeric, UniqueConstraint

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.stock import Stock

class Portfolio(Base):
    __table_args__ = {
        UniqueConstraint("user_id", "name", name="unique_portfolio_name_"),
    }
    user: Mapped["User"] = relationship(back_populates="portfolios")
    name: Mapped[str] = mapped_column(unique=True)
    cash_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    total_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    stocks: Mapped[list["Stock"]] = relationship("Stocks", back_populates="portfolio")
    is_active: Mapped[bool] = mapped_column(default=True)