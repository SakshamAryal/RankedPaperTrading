from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class TradeResponse(BaseModel):
    symbol: str
    type: str
    price_per_share: Decimal = Field(max_digits=10, decimal_places=2)
    quantity: Decimal = Field(max_digits=10, decimal_places=6)
    created_at: datetime = Field()


