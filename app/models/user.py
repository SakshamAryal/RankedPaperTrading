from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.models.base import Base
from decimal import Decimal
from sqlalchemy import Numeric

if TYPE_CHECKING:
    from app.models.portfolio import Portfolio
    from app.models.trade import Trade

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    cash_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=10000 )
    portfolios: Mapped[list["Portfolio"]] = relationship("Portfolio", back_populates="user")
    trade: Mapped[list['Trade']] = relationship("Trade", back_populates="user")
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    hashed_password: Mapped[str] = mapped_column()
