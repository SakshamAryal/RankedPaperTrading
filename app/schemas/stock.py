from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.trade import TradeResponse

class StockPriceResponse(BaseModel):
    symbol: str
    current_price: Decimal
    last_updated: datetime

class Stock(BaseModel):
    symbol: str
    quantity: Decimal

class StockResponse(Stock):
    avg_price: Decimal
    model_config = ConfigDict(from_attributes=True)

class StockTradeResponse(Stock):
    trades: list[TradeResponse]