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

def build_portfolio_response(portfolio: Portfolio, db: Session) -> PortfolioResponse:
    prices = get_prices(portfolio, db)
    holdings = [
        HoldingResponse(
            **StockResponse.model_validate(stock).model_dump(),
            current_price=prices[stock.symbol],
            market_value=(stock.quantity * prices[stock.symbol]).quantize(CENT, ROUND_HALF_UP),
        )
        for stock in portfolio.stocks
        if stock.quantity > 0
    ]
    total_value = portfolio.cash_balance + sum(h.market_value for h in holdings)
    return PortfolioResponse(
        **PortfolioStored.model_validate(portfolio).model_dump(),
        total_balance= total_value,
        stocks=holdings,
        return_percent= (((total_value - portfolio.net_deposited)/max(0.01,portfolio.net_deposited))*100).quantize(CENT, ROUND_HALF_UP),
    )