from datetime import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, Field, model_validator


class TradeResponse(BaseModel):
    symbol: str
    type: str
    price_per_share: Decimal = Field(max_digits=10, decimal_places=2)
    quantity: Decimal = Field(max_digits=10, decimal_places=6)
    created_at: datetime = Field()


class TradeCreate(BaseModel):
    symbol: str = Field(description="Stock ticker symbol e.g. AAPL")
    type: Literal["buy", "sell"]
    quantity: Decimal | None = Field(default=None, description="Number of shares",
                                     gt=0, max_digits=10, decimal_places=6)
    amount: Decimal | None = Field(default=None, description="Dollar amount to trade",
                                   gt=0, max_digits=10, decimal_places=2)

    @model_validator(mode="after")
    def check_quantity_xor_amount(self) -> "TradeCreate":
        if (self.quantity is None) == (self.amount is None):
            raise ValueError("Provide exactly one of 'quantity' or 'amount'")
        return self


