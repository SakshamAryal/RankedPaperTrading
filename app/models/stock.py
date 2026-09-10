from sqlalchemy import Numeric, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from app.models import Base
from sqlalchemy import ForeignKey
from decimal import Decimal


if TYPE_CHECKING:
    from app.models.portfolio import Portfolio
    from app.models.trade import Trade

class Stock(Base):
    __table_args__ = (
        UniqueConstraint("portfolio_id", "symbol", name="unique_portfolio_name_and_stock_name"),
    )
    symbol: Mapped[str] = mapped_column()
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 6))
    avg_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolio.id"))
    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="stocks")
    trades: Mapped[list["Trade"]] = relationship("Trade", back_populates="stock")
