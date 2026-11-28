"""
Unit tests: call the function directly with objects built in memory.
No database, no HTTP, no network. Models can be built without a session.
"""
from decimal import Decimal

import pytest

from app.models import Portfolio, Stock
from app.services.valuation import get_current_value, get_unit_price


def make_portfolio(cash="0", units="0", holdings=()):
    """holdings: (symbol, quantity) pairs."""
    return Portfolio(
        cash_balance=Decimal(cash),
        units=Decimal(units),
        stocks=[Stock(symbol=s, quantity=Decimal(q), avg_price=Decimal("1")) for s, q in holdings],
    )


def test_value_is_cash_when_no_holdings():
    portfolio = make_portfolio(cash="250.00")

    assert get_current_value(portfolio, prices={}) == Decimal("250.00")


def test_value_adds_holdings_at_current_price():
    portfolio = make_portfolio(cash="100.00", holdings=[("AAPL", "2"), ("MSFT", "0.5")])
    prices = {"AAPL": Decimal("150.00"), "MSFT": Decimal("400.00")}

    # 100 + 2*150 + 0.5*400
    assert get_current_value(portfolio, prices) == Decimal("600.00")


def test_value_skips_zero_quantity_holdings():
    # MSFT isn't in prices. If the function didn't skip it, this would raise KeyError.
    portfolio = make_portfolio(cash="10.00", holdings=[("MSFT", "0")])

    assert get_current_value(portfolio, prices={}) == Decimal("10.00")


# parametrize runs the same test once for each tuple
@pytest.mark.parametrize(
    "quantity, price, expected",
    [
        ("0.333333", "10.00", "3.33"),   # 3.33333 -> rounds down
        ("0.000500", "10.00", "0.01"),   # 0.005   -> HALF_UP rounds to 0.01
        ("0.000499", "10.00", "0.00"),   # 0.00499 -> rounds to 0.00
    ],
)
def test_value_rounds_half_up_to_cents(quantity, price, expected):
    portfolio = make_portfolio(holdings=[("AAPL", quantity)])

    assert get_current_value(portfolio, {"AAPL": Decimal(price)}) == Decimal(expected)


def test_unit_price_is_one_when_no_units():
    assert get_unit_price(make_portfolio(cash="500.00"), prices={}) == Decimal(1)
