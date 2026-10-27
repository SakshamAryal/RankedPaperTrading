from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class RefreshToken(Base):
    token: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    is_revoked: Mapped[bool] = mapped_column(default=False, server_default="false")
    expires_at: Mapped[datetime] = mapped_column()
