from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db_dependency import get_db
from app.dependencies.user_dependency import get_current_user
from app.models import Portfolio, User


def get_owned_portfolio(portfolio_id: int, user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)) -> Portfolio:
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id, Portfolio.user_id == user.id,
                                           Portfolio.is_active == True).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found.")
    return portfolio
