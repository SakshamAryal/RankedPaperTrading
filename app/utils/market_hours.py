import yfinance as yf
from fastapi import HTTPException
from yfinance.exceptions import YFRateLimitError, YFTickerMissingError


def is_open(symbol: str)->  str:
    info = valid_symbol(symbol)
    market_state = info["marketState"]
    return market_state

def valid_symbol(symbol: str) -> dict[str, str]:
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