from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from app.models import Portfolio
from app.schemas.portfolio import PortfolioStored, PortfolioResponse
from app.schemas.stock import HoldingResponse, StockResponse
from app.utils.price import get_current_price


# services/valuation.py
def get_prices(portfolio: Portfolio, db: Session) -> dict[str, Decimal]:
    return {
        stock.symbol: get_current_price(stock.symbol, db).current_price
        for stock in portfolio.stocks
        if stock.quantity > 0
    }

CENT = Decimal("0.01")

def build_portfolio_response(portfolio: Portfolio, prices: dict[str, Decimal]) -> PortfolioResponse:
    holdings = get_holdings(portfolio, prices)
    unit_price = get_unit_price(portfolio, prices)
    return PortfolioResponse(
        **PortfolioStored.model_validate(portfolio).model_dump(),
        total_balance= get_current_value(portfolio, prices),
        stocks=holdings,
        return_percent = ((unit_price - 1) *100).quantize(CENT, ROUND_HALF_UP) if portfolio.units > 0 else None,
    )

def get_current_value(portfolio: Portfolio, prices: dict[str, Decimal]) -> Decimal:
    stock_price = 0
    for stock in portfolio.stocks:
        if stock.quantity > 0:
            stock_price += prices[stock.symbol] * stock.quantity
    return (portfolio.cash_balance + stock_price).quantize(CENT, ROUND_HALF_UP)

def get_unit_price(portfolio: Portfolio, prices: dict[str, Decimal]) -> Decimal:
    total_value = get_current_value(portfolio, prices)
    if portfolio.units <= 0:
        return Decimal(1)
    unit_price = total_value / portfolio.units
    return unit_price

def get_holdings(portfolio: Portfolio, prices:dict[str, Decimal]) -> list[HoldingResponse]:
    return [
        HoldingResponse(
            **StockResponse.model_validate(stock).model_dump(),
            current_price=prices[stock.symbol],
            market_value=(stock.quantity * prices[stock.symbol]).quantize(CENT, ROUND_HALF_UP),
        )
        for stock in portfolio.stocks
        if stock.quantity > 0
    ]