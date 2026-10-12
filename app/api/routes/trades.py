from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db_dependency import get_db
from app.dependencies.user_dependency import get_current_user
from app.models.user import User
from app.models.portfolio import Portfolio
from app.models.stock import Stock
from app.models.trade import Trade
from app.schemas.stock import StockPriceResponse
from app.schemas.trade import TradeCreate, TradeResponse
from app.utils.price import get_current_price

trades = APIRouter(
    prefix="/trades",
    tags=["trades"],
)


@trades.get("/lookup/{symbol}", response_model=StockPriceResponse, status_code=200)
async def lookup_stock(symbol: str, db: Session = Depends(get_db)):
    return get_current_price(symbol, db)


@trades.post("/{portfolio_name}/trades/", response_model=TradeResponse, status_code=201)
async def create_trade(portfolio_name: str, trade: TradeCreate, user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.name == portfolio_name,
                                           Portfolio.user_id == user.id, Portfolio.is_active == True).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found.")

    symbol = trade.symbol.upper()
    stock_price = get_current_price(symbol, db)

    if trade.quantity is not None:
        quantity = trade.quantity
    else:
        quantity = (trade.amount / stock_price.current_price).quantize(Decimal("0.000001"), rounding=ROUND_DOWN)
        if quantity <= 0:
            raise HTTPException(status_code=400, detail="Amount too small to trade any shares.")

    cash_value = (quantity * stock_price.current_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    stock = db.query(Stock).filter(Stock.portfolio_id == portfolio.id, Stock.symbol == symbol).first()

    if trade.type == "buy":
        if portfolio.cash_balance < cash_value:
            raise HTTPException(status_code=400, detail="Insufficient funds.")
        if stock:
            new_quantity = stock.quantity + quantity
            stock.avg_price = ((stock.avg_price * stock.quantity) + cash_value) / new_quantity
            stock.quantity = new_quantity
        else:
            stock = Stock(symbol=symbol, quantity=quantity, avg_price=stock_price.current_price,
                          portfolio_id=portfolio.id)
            db.add(stock)
        portfolio.cash_balance -= cash_value
    else:
        if not stock or stock.quantity < quantity:
            raise HTTPException(status_code=400, detail="Insufficient shares.")
        stock.quantity -= quantity
        portfolio.cash_balance += cash_value

    db.flush()
    new_trade = Trade(symbol=symbol, type=trade.type, price_per_share=stock_price.current_price,
                      quantity=quantity, stock_id=stock.id)
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    return new_trade
