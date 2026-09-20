from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.trade import TradeResponse

class Stock(BaseModel):
    symbol: str
    quantity: Decimal

class StockTrade(Stock):
    symbol: str = Field(description="Stock ticker symbol e.g. AAPL")
    quantity: Decimal = Field(description="Stock quantity",
                              ge=0, max_digits=10, decimal_places=6)

class StockResponse(Stock):
    avg_price: Decimal
    model_config = ConfigDict(from_attributes=True)

class StockTradeResponse(Stock):
    trades: list[TradeResponse]