from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio
from app.models.stock import Stock
from app.models.trade import Trade
from app.schemas.trade import TradeCreate
from app.utils.price import get_current_price
from app.models import StockPrice
from app.utils.market_hours import is_open


def execute_trade(portfolio: Portfolio, trade: TradeCreate, db: Session) -> Trade:
    symbol = trade.symbol.upper()

    market_status = is_open(symbol)
    if market_status != "REGULAR":
        raise HTTPException(status_code=409, detail=f"Market closed for {symbol}")

    stock_price = get_current_price(symbol, db)
    quantity = get_quantity(trade, stock_price)
    stock = db.query(Stock).filter(Stock.portfolio_id == portfolio.id, Stock.symbol == symbol).first()

    if trade.type == "buy":
        stock = buy(stock, stock_price, quantity, portfolio)
    else:
        sell(stock, stock_price, quantity, portfolio)
    db.flush()
    new_trade = Trade(symbol=symbol, type=trade.type, price_per_share=stock_price.current_price,
                      quantity=quantity, stock_id=stock.id)
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    return new_trade

def buy(stock: Optional[Stock], stock_price: StockPrice, quantity: Decimal, portfolio: Portfolio) -> Stock:
    cash_value = get_cash_value(quantity, stock_price.current_price)
    if portfolio.cash_balance < cash_value:
        raise HTTPException(status_code=400, detail="Insufficient funds.")

    if not stock:
        stock = Stock(symbol=stock_price.symbol, quantity=Decimal(0), avg_price=stock_price.current_price,
                      portfolio_id=portfolio.id)
        portfolio.stocks.append(stock)

    new_quantity = stock.quantity + quantity
    stock.avg_price = ((((stock.avg_price * stock.quantity) + cash_value) / new_quantity)
                       .quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    stock.quantity = new_quantity
    portfolio.cash_balance -= cash_value
    return stock


def sell(stock: Optional[Stock], stock_price: StockPrice, quantity: Decimal, portfolio: Portfolio):
    if not stock or stock.quantity < quantity:
        raise HTTPException(status_code=400, detail="Insufficient shares.")
    stock.quantity -= quantity
    portfolio.cash_balance += get_cash_value(quantity, stock_price.current_price)


def get_cash_value(quantity: Decimal, current_price : Decimal) -> Decimal :
    return (quantity * current_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def get_quantity(trade: TradeCreate, stock_price: StockPrice) -> Decimal:
    if trade.quantity is not None:
        quantity = trade.quantity
    else:
        quantity = (trade.amount / stock_price.current_price).quantize(Decimal("0.000001"), rounding=ROUND_DOWN)
        if quantity <= 0:
            raise HTTPException(status_code=400, detail="Amount too small to trade any shares.")
    return quantity