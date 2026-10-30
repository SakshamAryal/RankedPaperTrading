# Ranked Paper Trading

A multi-user paper-trading REST API. Each user starts with $10,000 of virtual cash, splits it across portfolios, and buys and sells real stocks at live market prices — no real money involved.

**Live API:** https://rankedpapertrading.onrender.com — try it from the interactive docs at [/docs](https://rankedpapertrading.onrender.com/docs).

## Features

- **Auth** — signup, login, short-lived JWT access tokens and 7-day refresh tokens. Refresh tokens are stored server-side, rotated on every refresh and revoked on logout; a refresh token can't be used to call protected routes.
- **Portfolios** — create, rename, deposit, withdraw and delete (soft delete). Names are unique per user, and a deleted portfolio's name can be reused.
- **Trading** — buy or sell by share count or by dollar amount, with fractional shares. Prices come from Yahoo Finance and are cached for 60 seconds.
- **Money handled as `Decimal`, never float** — cash rounds half-up to cents; share quantities from a dollar-amount buy round down to 6 decimal places.
- **Ownership checks** — users can only see and change their own portfolios; anyone else's returns 404.

## Stack

- **FastAPI**
- **PostgreSQL** with **SQLAlchemy 2.0** and **Alembic** migrations
- **yfinance** for market prices
- **python-jose** for JWTs, **pwdlib** (argon2) for password hashing
- **Pydantic** for request validation
- Hosted on **Render**

## Running locally

Requires Python 3.13+ and a running PostgreSQL server.

1. Clone the repo and install dependencies:

   ```bash
   git clone https://github.com/SakshamAryal/RankedPaperTrading.git
   cd RankedPaperTrading
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create a database, then copy the example settings and fill them in:

   ```bash
   cp .env.example .env
   ```

   | Variable | Example |
   |---|---|
   | `DATABASE_URL` | `postgresql+psycopg://user:password@localhost:5432/paper_trading` |
   | `SECRET_KEY` | any long random string, e.g. from `openssl rand -hex 32` |
   | `ALGORITHM` | `HS256` |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
   | `REFRESH_TOKEN_EXPIRE_DAYS` | `7` |

3. Create the tables and start the server:

   ```bash
   alembic upgrade head
   uvicorn app.main:app --reload
   ```

Interactive API docs are at http://127.0.0.1:8000/docs.

## Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/users` | Sign up |
| `GET` | `/users/me` | Current user |
| `POST` | `/auth/token` | Log in (form data) — returns access and refresh tokens |
| `POST` | `/auth/refresh` | Swap a refresh token for a new pair |
| `POST` | `/auth/logout` | Revoke a refresh token |
| `GET` | `/portfolios` | List your portfolios |
| `POST` | `/portfolios` | Create a portfolio, funded from your cash |
| `GET` | `/portfolios/{id}` | Portfolio with its holdings |
| `PATCH` | `/portfolios/{id}` | Rename |
| `POST` | `/portfolios/{id}/deposit` | Move cash into the portfolio |
| `POST` | `/portfolios/{id}/withdraw` | Move cash back out |
| `DELETE` | `/portfolios/{id}` | Delete an empty portfolio |
| `GET` | `/portfolios/{id}/trades` | Trade history |
| `POST` | `/portfolios/{id}/trades` | Buy or sell |
| `GET` | `/stocks/{symbol}` | Current price |

## Example requests

These run against the live API. To use a local server instead, set `BASE_URL=http://127.0.0.1:8000`.

```bash
BASE_URL=https://rankedpapertrading.onrender.com
```

Sign up and log in. Usernames are shared on the live API, so pick your own instead of `alice`:

```bash
curl -X POST $BASE_URL/users \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "password123"}'

curl -X POST $BASE_URL/auth/token \
  -d "username=alice&password=password123"
```

Put the returned `access_token` in a variable for the rest:

```bash
TOKEN=<access_token>
```

Create a portfolio with $2,000:

```bash
curl -X POST $BASE_URL/portfolios \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Tech", "cash_balance": "2000"}'
```

Buy $500 of Apple, then sell 1 share (use the `id` from the create response):

```bash
curl -X POST $BASE_URL/portfolios/1/trades \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "type": "buy", "amount": "500"}'

curl -X POST $BASE_URL/portfolios/1/trades \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "type": "sell", "quantity": "1"}'
```

Look up a price:

```bash
curl $BASE_URL/stocks/MSFT
```

## Future work

- **Leaderboards** — rank users by net worth, then by all-time and weekly return %, with daily snapshots for the weekly figures.
- **Redis** — move the price cache from Postgres to Redis with a TTL, and keep the leaderboards in sorted sets.
- **WebSockets** — push live price and leaderboard updates, driven by Redis pub/sub.
- **Live portfolio value** — keep each portfolio's total value up to date as prices move.
- **Tests** — a pytest suite for the money rules, auth and ownership checks, plus row locking for simultaneous trades.
- **Docker Compose** — run the API, Postgres and Redis with one command.
- **Discord bot** for trading from chat.
