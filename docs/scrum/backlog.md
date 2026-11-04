# Product Backlog — Ranked Paper Trading

Tickets are numbered by epic: `B` = bug, `US` = user story, `T` = task.
Move a ticket into a sprint file when it's committed to that sprint.

| Epic | Goal | Tickets |
|---|---|---|
| **Epic 1: Correctness** | The money logic can't be broken | In Sprint 01 |
| **Epic 2: Leaderboards** | Players can be ranked | US2.001–002 in Sprint 01; US2.003–005 in backlog |
| **Epic 3: Quality & Deploy** | Tested, documented, running | T3.001 – T3.006 |
| **Epic 4: Extras** | Real-time and integrations | US4.001 – US4.004 |

---

## Epic 1: Correctness
> **Goal:** No bug can create or lose money.\
> *All tickets moved to Sprint 01.*
```

```

---

## Epic 2: Leaderboards
> **Goal:** Players can be ranked by net worth, all-time return, and weekly return.
> *US2.001, US2.002 moved to Sprint 01.*

```
--------------------------------------------------------------------------
TYPE     : USER STORY US2.001 : Not Started
NAME     : Portfolio current value and return
PRIORITY : 1
ESTIMATE : 3 hours   ACTUAL : -
AS A     : player
I WANT   : to see each portfolio's current value and return %
SO THAT  : I know how my trades are doing
ACCEPTANCE:
  - value = cash + sum(quantity x StockPrice.current_price)
  - return % = (value - net_deposited) / net_deposited
  - Deposits and withdrawals do not change return %
  - Shown in PortfolioResponse
NOTES    : Read prices from the StockPrice table, not yfinance per
           holding. One reusable function; every leaderboard builds on it.
--------------------------------------------------------------------------
TYPE     : USER STORY US2.002 : Not Started
NAME     : Periodic portfolio snapshots
PRIORITY : 1
ESTIMATE : 4 hours   ACTUAL : -
AS A     : system
I WANT   : to record every active portfolio's value on a schedule
SO THAT  : weekly returns can be computed from real history
ACCEPTANCE:
  - Snapshot table: portfolio_id, value, net_deposited, taken_at
  - Job runs on a fixed interval (e.g. hourly) while the app is up
  - Prices for held symbols refreshed before snapshotting
  - One failing symbol does not stop the whole run
NOTES    : START EARLY. Missing history can't be rebuilt later.
           Consider APScheduler, started from FastAPI lifespan.
--------------------------------------------------------------------------
```

---

## Epic 3: Quality & Deploy
> **Goal:** The API is tested, documented, and anyone can run it.

```
--------------------------------------------------------------------------
TYPE     : TASK T3.001 : Not Started
NAME     : pytest setup
PRIORITY : 1
ESTIMATE : 4 hours   ACTUAL : -
GOAL     : Test infrastructure every other test ticket builds on.
ACCEPTANCE:
  - conftest.py with TestClient, test DB, per-test cleanup
  - yfinance mocked (no network in tests)
  - Fixtures for an authenticated user and a funded portfolio
NOTES    : Use real Postgres, not SQLite (FOR UPDATE and partial
           indexes behave differently).
--------------------------------------------------------------------------
TYPE     : TASK T3.002 : Not Started
NAME     : Trade tests
PRIORITY : 1
ESTIMATE : 3 hours   ACTUAL : -
ACCEPTANCE:
  - Buy/sell by quantity and by amount
  - Insufficient funds and insufficient shares
  - Concurrent buy race test (B1.001)
--------------------------------------------------------------------------
TYPE     : TASK T3.003 : Not Started
NAME     : Portfolio and auth tests
PRIORITY : 2
ESTIMATE : 3 hours   ACTUAL : -
ACCEPTANCE:
  - Negative/zero transfers rejected; delete rules (B1.004)
  - Same name allowed across users, rejected for the same user
  - Refresh token rejected as access token; rotation; logout
--------------------------------------------------------------------------
TYPE     : TASK T3.004 : Not Started
NAME     : Leaderboard tests
PRIORITY : 2
ESTIMATE : 2 hours   ACTUAL : -
ACCEPTANCE:
  - Ordering correct for known prices
  - Deposits do not change return % or rank
--------------------------------------------------------------------------
TYPE     : TASK T3.005 : Not Started
NAME     : Docker and Compose
PRIORITY : 2
ESTIMATE : 2 hours   ACTUAL : -
ACCEPTANCE:
  - Dockerfile builds and runs the API
  - docker-compose up starts API + Postgres and runs migrations
--------------------------------------------------------------------------
TYPE     : TASK T3.006 : Not Started
NAME     : README and deploy
PRIORITY : 2
ESTIMATE : 2 hours   ACTUAL : -
ACCEPTANCE:
  - README: what it is, setup, env vars, endpoints, design decisions
  - Live deployment updated with all migrations applied
--------------------------------------------------------------------------
```

---

## Epic 4: Extras
> **Goal:** Real-time updates and integrations. Start only after Epics 1–3 ship.
> Acceptance criteria get written when a ticket moves into a sprint.

```
--------------------------------------------------------------------------
TYPE     : USER STORY US4.001 : Not Started
NAME     : Redis price cache
PRIORITY : 4
ESTIMATE : 3 hours   ACTUAL : -
AS A     : system
I WANT   : current prices cached in Redis with a TTL
SO THAT  : price reads don't hit Postgres or yfinance every time
--------------------------------------------------------------------------
TYPE     : USER STORY US4.002 : Not Started
NAME     : Leaderboards in Redis sorted sets
PRIORITY : 4
ESTIMATE : 4 hours   ACTUAL : -
AS A     : player
I WANT   : leaderboards to load instantly
SO THAT  : the app feels fast as users grow
--------------------------------------------------------------------------
TYPE     : USER STORY US4.003 : Not Started
NAME     : Live leaderboard over WebSocket
PRIORITY : 5
ESTIMATE : 5 hours   ACTUAL : -
AS A     : player
I WANT   : rank changes pushed to me live
SO THAT  : I don't have to refresh
--------------------------------------------------------------------------
TYPE     : USER STORY US4.004 : Not Started
NAME     : Discord bot
PRIORITY : 6
ESTIMATE : 5 hours   ACTUAL : -
AS A     : player
I WANT   : to check prices and leaderboards from Discord
SO THAT  : I can play without opening the app
--------------------------------------------------------------------------
```