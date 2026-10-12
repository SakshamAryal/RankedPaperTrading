from fastapi import FastAPI
from app.api.routes.auth import auth
from app.api.routes.users import users
from app.api.routes.portfolios import portfolios
from app.api.routes.trades import trades

app = FastAPI()
app.include_router(auth)
app.include_router(users)
app.include_router(portfolios)
app.include_router(trades)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
