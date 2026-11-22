from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict
from decimal import Decimal

from app.schemas.stock import HoldingResponse


class Portfolio(BaseModel):
    name: str
    cash_balance: Decimal


class PortfolioCreate(Portfolio):
    name: str = Field(min_length=3, max_length=50)
    cash_balance: Decimal = Field(max_digits=10, decimal_places=2, gt=0.00)


class PortfolioStored(Portfolio):
    id: int
    net_deposited: Decimal
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PortfolioResponse(PortfolioStored):
    total_balance: Decimal = Field(max_digits=10, decimal_places=2, ge=0.00)
    stocks: list[HoldingResponse]

class PortfolioChangeName(BaseModel):
    name: str = Field(min_length=3, max_length=50)


class FundsTransfer(BaseModel):
    amount: Decimal = Field(max_digits=10, decimal_places=2, gt=0.00)
