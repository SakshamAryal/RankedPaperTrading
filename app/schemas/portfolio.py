from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from pydantic import computed_field

from app.schemas.stock import StockResponse

class Portfolio(BaseModel):
    name: str
    cash_balance: Decimal


class PortfolioCreate(Portfolio):
    name: str = Field(min_length=3, max_length=50)
    cash_balance: Decimal = Field(max_digits=10, decimal_places=2, gt=0.00)


class PortfolioResponse(Portfolio):
    id: int
    net_deposited: Decimal
    created_at: datetime
    stocks: list[StockResponse]

    @field_validator("stocks")
    @classmethod
    def hide_sold_out(cls, stocks: list[StockResponse]) -> list[StockResponse]:
        # a sold-out holding keeps its row (trades reference it) but isn't shown
        return [stock for stock in stocks if stock.quantity > 0]

    @computed_field()
    @property
    def total_balance(self) -> Decimal:
        stocks_total_balance = Decimal(0)
        for stock in self.stocks:
            stocks_total_balance += stock.quantity*stock.current_price
        return stocks_total_balance + self.cash_balance

class PortfolioChangeName(BaseModel):
    name: str = Field(min_length=3, max_length=50)


class FundsTransfer(BaseModel):
    amount: Decimal = Field(max_digits=10, decimal_places=2, gt=0.00)
