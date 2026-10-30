from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio
from app.models.stock import Stock
from app.models.trade import Trade
from app.schemas.trade import TradeCreate
from app.utils.price import get_current_price


def execute_trade(portfolio: Portfolio, trade: TradeCreate, db: Session) -> Trade:
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
            stock.avg_price = (((stock.avg_price * stock.quantity) + cash_value) / new_quantity).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
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
