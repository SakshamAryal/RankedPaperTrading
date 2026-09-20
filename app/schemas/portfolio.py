from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal
from app.schemas.stock import StockResponse

class Portfolio(BaseModel):
    name: str
    cash_balance: Decimal


class PortfolioCreate(Portfolio):
    name: str = Field(min_length=3, max_length=50)
    cash_balance: Decimal = Field(max_digits=10, decimal_places=2, ge=0.00)


class PortfolioResponse(Portfolio):
    total_balance: Decimal
    created_at: datetime
    stocks: list[StockResponse]


class PortfolioChangeName(BaseModel):
    name: str = Field(min_length=3, max_length=50)


class FundsTransfer(Portfolio):
    amount: Decimal = Field(max_digits=10, decimal_places=2, ge=0.00)

