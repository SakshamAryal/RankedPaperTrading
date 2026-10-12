from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class StockPrice(Base):
    symbol: Mapped[str] = mapped_column(unique=True)
    current_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    last_updated: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
