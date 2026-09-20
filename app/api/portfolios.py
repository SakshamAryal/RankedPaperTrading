from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.user_dependency import get_current_user
from app.dependencies.db_dependency import get_db
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse, FundsTransfer
from app.models.user import User
from app.models.portfolio import Portfolio

portfolios = APIRouter(
    prefix="/portfolios",
    tags=["portfolios"],
)

@portfolios.get("/info", response_model=list[PortfolioResponse], status_code=200)
async def get_portfolios(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_portfolios = db.query(Portfolio).filter(Portfolio.user_id == user.id,
                                                 Portfolio.is_active == True).all()

    return user_portfolios


@portfolios.post("/create_portfolio", response_model=PortfolioResponse)
async def create_portfolio(new_portfolio: PortfolioCreate, user: User = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if user.cash_balance - new_portfolio.cash_balance < 0:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    portfolio = Portfolio(
        name =new_portfolio.name,
        user_id = user.id,
        cash_balance = new_portfolio.cash_balance,
        total_balance = new_portfolio.cash_balance,

    )
    db.add(portfolio)
    user.cash_balance -= new_portfolio.cash_balance
    db.commit()
    db.refresh(portfolio)
    return portfolio


@portfolios.put("/{portfolio_name}/deposit/{amount}", response_model=PortfolioResponse, status_code=200)
async def deposit_cash(amount: Decimal, portfolio_name: str, user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.name == portfolio_name,
                                           Portfolio.user_id == user.id, Portfolio.is_active == True).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found.")
    if user.cash_balance - amount < 0:
        raise HTTPException(status_code=400, detail="Insufficient funds.")
    portfolio.cash_balance += amount
    portfolio.total_balance += amount
    user.cash_balance -= amount
    db.commit()
    db.refresh(portfolio)
    return portfolio

@portfolios.put("/{portfolio_name}/withdraw/{amount}", response_model=PortfolioResponse, status_code=200)
async def withdraw_cash(amount: Decimal, portfolio_name: str, user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.name == portfolio_name,
                                           Portfolio.user_id == user.id, Portfolio.is_active == True).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found.")
    if portfolio.cash_balance - amount < 0:
        raise HTTPException(status_code=400, detail="Insufficient funds.")
    portfolio.cash_balance -= amount
    portfolio.total_balance -= amount
    user.cash_balance += amount
    db.commit()
    db.refresh(portfolio)
    return portfolio


@portfolios.delete("/{portfolio_name}/", status_code=200)
async def delete_portfolio(portfolio_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.name == portfolio_name,
                                           Portfolio.user_id == user.id, Portfolio.is_active == True).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found.")
    if portfolio.total_balance > 0:
        raise HTTPException(status_code=400, detail="Can't delete portfolio with funds in it.")
    portfolio.is_active = False
    db.commit()
    db.refresh(portfolio)
    return {"message": "Portfolio deleted successfully"}
