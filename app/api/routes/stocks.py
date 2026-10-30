from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db_dependency import get_db
from app.schemas.stock import StockPriceResponse
from app.utils.price import get_current_price

stocks = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
)


@stocks.get("/{symbol}", response_model=StockPriceResponse, status_code=200)
def lookup_stock(symbol: str, db: Session = Depends(get_db)):
    return get_current_price(symbol, db)
