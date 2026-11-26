import yfinance as yf
from fastapi import HTTPException


def is_open(symbol: str)-> bool | str:
    ticker = yf.Ticker(symbol)
    history = ticker.history(period="1d")
    if history.empty:
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found")
    market_state = history.market_state
    return market_state

