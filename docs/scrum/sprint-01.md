# Sprint 01 — Nov 4 to Nov 18, 2026

**Sprint Goal:** No bug can create or lose money, and portfolio snapshots are recording.
**Capacity:** ~8h (midterms)
| Ticket | Name | Est | Actual | Status |
|---|---|---|---|---|
| B1.001 | Concurrent trades can double-spend | 3h | | Not Started |
| B1.002 | Concurrent deposit/withdraw can create cash | 2h | | Not Started |
| B1.003 | /users/me never returns portfolios | 0.5h | | Not Started |
| B1.004 | Portfolio can't be deleted after a losing trade | 2h | | Not Started |
| T1.005 | Remove total_balance column | 1.5h | | Not Started |
| US2.001 | Portfolio current value and return | 3h | | Not Started |
| US2.002 | Periodic portfolio snapshots | 4h | | Not Started |
| **Total** | | **16h** | | |

**Suggested order:** B1.003 (warm-up) → B1.001 → B1.002 → US2.001 → US2.002 → B1.004 → T1.005
Aim to have US2.002 running by about Nov 11 so snapshot history starts building.

---

## Tickets

```
--------------------------------------------------------------------------
TYPE     : BUG B1.001 : Not Started
NAME     : Concurrent trades can double-spend
PRIORITY : 1
ESTIMATE : 3 hours   ACTUAL : -
PROBLEM  : Two simultaneous buys on the same portfolio both pass the
           funds check because neither locks the portfolio row.
EXPECTED : Trades on one portfolio are serialized; cash never goes negative.
ACCEPTANCE:
  - Two parallel buys at 60% of cash each -> one 201, one 400
  - Price is fetched before the lock is taken
  - Trades on different portfolios do not block each other
NOTES    : app/services/trade.py. get_current_price commits, which
           releases locks. Use db.refresh(portfolio, with_for_update=True).
--------------------------------------------------------------------------
TYPE     : BUG B1.002 : Not Started
NAME     : Concurrent deposit/withdraw can create cash
PRIORITY : 1
ESTIMATE : 2 hours   ACTUAL : -
PROBLEM  : Deposit and withdraw read-check-write user.cash_balance and
           portfolio.cash_balance without locks.
EXPECTED : Parallel transfers never overdraw the user or the portfolio.
ACCEPTANCE:
  - Two parallel deposits at 60% of user cash -> one 200, one 400
  - Two parallel withdrawals at 60% of portfolio cash -> one 200, one 400
  - Locks always taken in the same order (user, then portfolio)
NOTES    : app/api/routes/portfolios.py. A consistent lock order
           prevents deadlocks.
--------------------------------------------------------------------------
TYPE     : BUG B1.003 : Not Started
NAME     : /users/me never returns portfolios
PRIORITY : 2
ESTIMATE : 0.5 hours   ACTUAL : -
PROBLEM  : UserResponse has field `portfolio`; model attribute is
           `portfolios`, so the field is always null.
EXPECTED : /me lists the user's active portfolios.
ACCEPTANCE:
  - /me returns a `portfolios` list
  - Soft-deleted portfolios are not included
NOTES    : app/schemas/user.py, app/models/user.py
--------------------------------------------------------------------------
TYPE     : BUG B1.004 : Not Started
NAME     : Portfolio can't be deleted after a losing trade
PRIORITY : 1
ESTIMATE : 2 hours   ACTUAL : -
PROBLEM  : Delete checks total_balance, which trades never update. After
           a loss and full withdrawal, total_balance stays > 0.
EXPECTED : Delete is allowed when the portfolio holds no cash and no shares.
ACCEPTANCE:
  - cash_balance == 0 and no holdings with quantity > 0 -> 204
  - Any cash or any shares left -> 400 with a clear message
  - Lose money, sell all, withdraw all -> delete succeeds
NOTES    : app/api/routes/portfolios.py
--------------------------------------------------------------------------
TYPE     : TASK T1.005 : Not Started
NAME     : Remove total_balance column
PRIORITY : 2
ESTIMATE : 1.5 hours   ACTUAL : -
GOAL     : Drop the misleading field now that net_deposited and computed
           value replace it.
ACCEPTANCE:
  - Alembic migration drops the column; downgrade restores it
  - Removed from model, PortfolioResponse, and all routes
  - Migration applied on Supabase
NOTES    : Do after B1.004 so nothing still reads it.
--------------------------------------------------------------------------
TYPE     : USER STORY US2.003 : Not Started
NAME     : Net worth leaderboard
PRIORITY : 2
ESTIMATE : 2 hours   ACTUAL : -
AS A     : player
I WANT   : to see users ranked by total net worth
SO THAT  : I can compare myself with others
ACCEPTANCE:
  - GET /leaderboard/net-worth
  - net worth = user cash + sum of active portfolio values
  - Returns rank, username, net worth; supports ?limit=
NOTES    : Include user cash; otherwise moving money in and out of
           portfolios changes rank.
--------------------------------------------------------------------------
TYPE     : USER STORY US2.004 : Not Started
NAME     : All-time return leaderboard
PRIORITY : 2
ESTIMATE : 2 hours   ACTUAL : -
AS A     : player
I WANT   : to see users ranked by all-time return %
SO THAT  : skill is rewarded, not just starting balance
ACCEPTANCE:
  - GET /leaderboard/all-time
  - Per user: (sum value - sum net_deposited) / sum net_deposited
  - Users with no deposits are excluded
--------------------------------------------------------------------------
TYPE     : USER STORY US2.005 : Not Started
NAME     : Weekly return leaderboard
PRIORITY : 3
ESTIMATE : 3 hours   ACTUAL : -
AS A     : player
I WANT   : to see who performed best in the last 7 days
SO THAT  : new players can compete with established ones
ACCEPTANCE:
  - GET /leaderboard/week
  - Baseline = snapshot closest to 7 days ago
  - Deposits/withdrawals during the week are not counted as gains
  - Portfolios with no baseline snapshot are excluded
NOTES    : Depends on US2.002 having run for a week.
--------------------------------------------------------------------------
```

---

## Sprint Review  *(fill in Nov 18)*
**Goal met?** Yes / Partly / No
**Done:**
**Not done (back to backlog):**
**Demo notes:**

## Sprint Retro  *(fill in Nov 18)*
**Estimate vs actual:** __h estimated / __h actual → ratio __
**What went well:**
**What didn't:**
**One thing to change next sprint:**