from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING
from app.models.base import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import ForeignKey, Index, Numeric, text

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.stock import Stock

class Portfolio(Base):
    __table_args__ = (
        # names are unique per user among active portfolios, so a deleted portfolio's name can be reused
        Index("unique_active_portfolio_name", "user_id", "name", unique=True, postgresql_where=text("is_active")),
    )
    name: Mapped[str] = mapped_column()
    cash_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    total_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    net_deposited: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="portfolios")
    stocks: Mapped[list["Stock"]] = relationship("Stock", back_populates="portfolio")
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")