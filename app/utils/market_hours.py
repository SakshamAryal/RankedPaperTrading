from typing import Any
import yfinance as yf
from fastapi import HTTPException
from yfinance.exceptions import YFRateLimitError, YFTickerMissingError


def get_market_state(symbol: str)->  str | None:
    info = get_symbol_info(symbol)
    market_state = info.get("marketState")
    return market_state

def get_symbol_info(symbol: str) -> dict[str, Any]:
    try:
        info = yf.Ticker(symbol).info
    except YFRateLimitError:
        raise HTTPException(status_code=503, detail="Try again later")
    except YFTickerMissingError:
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found")
    except Exception:
        raise HTTPException(status_code=503, detail="Couldn't check right now")
    if not info.get("quoteType"):
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found")
    return info
