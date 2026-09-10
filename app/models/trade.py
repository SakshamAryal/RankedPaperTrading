from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from app.models import Base
from sqlalchemy import ForeignKey
from decimal import Decimal


if TYPE_CHECKING:
    from app.models.stock import Stock

class Trade(Base):
    __tablename__ = "trade"
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column(
        CheckConstraint("type IN ('buy', 'sell')")
    )
    price_per_share: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 6))
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    stock: Mapped["Stock"] = relationship("stock", back_populates="trades")
    stock_id: Mapped[int] = mapped_column(ForeignKey("Stock.id"))
