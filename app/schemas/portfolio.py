from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal
from app.schemas.stock import StockResponse


class PortfolioCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    cash_balance: Decimal = Field(max_digits=10, decimal_places=2, ge=0.00)


class PortfolioResponse(BaseModel):
    name: str
    cash_balance: Decimal
    total_balance: Decimal
    created_at: datetime
    stocks: list[StockResponse]



