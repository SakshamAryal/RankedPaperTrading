from datetime import datetime, timedelta, timezone
from decimal import Decimal

import yfinance as yf
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.stock_price import StockPrice

PRICE_STALE_AFTER = timedelta(minutes=1)


def _fetch_price(symbol: str) -> Decimal:
    ticker = yf.Ticker(symbol)
    history = ticker.history(period="1d")
    if history.empty:
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found")
    return Decimal(str(round(history["Close"].iloc[-1], 2)))


def get_current_price(symbol: str, db: Session) -> StockPrice:
    symbol = symbol.upper()
    stock_price = db.query(StockPrice).filter(StockPrice.symbol == symbol).first()
    now = datetime.now(timezone.utc)

    if stock_price and now - stock_price.last_updated.replace(tzinfo=timezone.utc) < PRICE_STALE_AFTER:
        return stock_price

    price = _fetch_price(symbol)
    if stock_price:
        stock_price.current_price = price
        stock_price.last_updated = now
    else:
        stock_price = StockPrice(symbol=symbol, current_price=price, last_updated=now)
        db.add(stock_price)
    db.commit()
    db.refresh(stock_price)
    return stock_price
