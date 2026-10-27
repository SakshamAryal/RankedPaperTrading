from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies.user_dependency import get_current_user
from app.dependencies.db_dependency import get_db
from app.dependencies.portfolio_dependency import get_owned_portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse, PortfolioChangeName, FundsTransfer
from app.models.user import User
from app.models.portfolio import Portfolio

portfolios = APIRouter(
    prefix="/portfolios",
    tags=["portfolios"],
)


def ensure_name_available(name: str, user: User, db: Session) -> None:
    taken = db.query(Portfolio).filter(Portfolio.user_id == user.id, Portfolio.name == name,
                                       Portfolio.is_active == True).first()
    if taken:
        raise HTTPException(status_code=409, detail="A portfolio with that name already exists.")


def commit_or_409(db: Session) -> None:
    # the name check above can race with another request; the unique index has the final say
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A portfolio with that name already exists.")


@portfolios.get("", response_model=list[PortfolioResponse], status_code=200)
def get_portfolios(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Portfolio).filter(Portfolio.user_id == user.id, Portfolio.is_active == True).all()


@portfolios.post("", response_model=PortfolioResponse, status_code=201)
def create_portfolio(new_portfolio: PortfolioCreate, user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    if user.cash_balance - new_portfolio.cash_balance < 0:
        raise HTTPException(status_code=400, detail="Insufficient funds.")
    ensure_name_available(new_portfolio.name, user, db)
    portfolio = Portfolio(
        name=new_portfolio.name,
        user_id=user.id,
        cash_balance=new_portfolio.cash_balance,
        total_balance=new_portfolio.cash_balance,
        net_deposited=new_portfolio.cash_balance,
    )
    db.add(portfolio)
    user.cash_balance -= new_portfolio.cash_balance
    commit_or_409(db)
    db.refresh(portfolio)
    return portfolio


@portfolios.get("/{portfolio_id}", response_model=PortfolioResponse, status_code=200)
def get_portfolio(portfolio: Portfolio = Depends(get_owned_portfolio)):
    return portfolio


@portfolios.patch("/{portfolio_id}", response_model=PortfolioResponse, status_code=200)
def rename_portfolio(change: PortfolioChangeName, portfolio: Portfolio = Depends(get_owned_portfolio),
                     user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if change.name != portfolio.name:
        ensure_name_available(change.name, user, db)
        portfolio.name = change.name
        commit_or_409(db)
        db.refresh(portfolio)
    return portfolio


@portfolios.post("/{portfolio_id}/deposit", response_model=PortfolioResponse, status_code=200)
def deposit_cash(transfer: FundsTransfer, portfolio: Portfolio = Depends(get_owned_portfolio),
                 user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.cash_balance - transfer.amount < 0:
        raise HTTPException(status_code=400, detail="Insufficient funds.")
    portfolio.cash_balance += transfer.amount
    portfolio.total_balance += transfer.amount
    portfolio.net_deposited += transfer.amount
    user.cash_balance -= transfer.amount
    db.commit()
    db.refresh(portfolio)
    return portfolio


@portfolios.post("/{portfolio_id}/withdraw", response_model=PortfolioResponse, status_code=200)
def withdraw_cash(transfer: FundsTransfer, portfolio: Portfolio = Depends(get_owned_portfolio),
                  user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if portfolio.cash_balance - transfer.amount < 0:
        raise HTTPException(status_code=400, detail="Insufficient funds.")
    portfolio.cash_balance -= transfer.amount
    portfolio.total_balance -= transfer.amount
    portfolio.net_deposited -= transfer.amount
    user.cash_balance += transfer.amount
    db.commit()
    db.refresh(portfolio)
    return portfolio


@portfolios.delete("/{portfolio_id}", status_code=204)
def delete_portfolio(portfolio: Portfolio = Depends(get_owned_portfolio), db: Session = Depends(get_db)):
    if portfolio.total_balance > 0:
        raise HTTPException(status_code=400, detail="Can't delete portfolio with funds in it.")
    portfolio.is_active = False
    db.commit()
