from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db_dependency import get_db
from app.dependencies.portfolio_dependency import get_owned_portfolio
from app.models.portfolio import Portfolio
from app.models.stock import Stock
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeResponse
from app.services.trade import execute_trade

trades = APIRouter(
    prefix="/portfolios/{portfolio_id}/trades",
    tags=["trades"],
)


@trades.get("", response_model=list[TradeResponse], status_code=200)
def get_trades(portfolio: Portfolio = Depends(get_owned_portfolio), db: Session = Depends(get_db)):
    return (db.query(Trade).join(Stock).filter(Stock.portfolio_id == portfolio.id)
            .order_by(Trade.created_at.desc()).all())


@trades.post("", response_model=TradeResponse, status_code=201)
def create_trade(trade: TradeCreate, portfolio: Portfolio = Depends(get_owned_portfolio),
                 db: Session = Depends(get_db)):
    return execute_trade(portfolio, trade, db)
