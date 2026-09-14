from pydantic import BaseModel,EmailStr, SecretStr, Field, ConfigDict
from decimal import Decimal

from app.schemas.portfolio import PortfolioResponse

class User(BaseModel):
    username: str
    email: EmailStr

class UserCreate(User):
    username: str = Field(min_length=3, max_length=20, description="Username")
    password: SecretStr = Field(min_length=8, description="Minimum of 8 characters")


class UserResponse(User):
    cash_balance: Decimal = Field(max_digits=10, decimal_places=2)
    portfolio: list[PortfolioResponse] | None = None
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(User):
    username: str | None = Field(None, min_length=3, max_length=20)
    email: EmailStr | None = None
    password: SecretStr | None = Field(None, min_length=8)
