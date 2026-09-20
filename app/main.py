from fastapi import FastAPI, APIRouter
from app.api.auth import auth
from app.api.users import users
from app.api.portfolios import portfolios

app = FastAPI()
app.include_router(auth)
app.include_router(users)
app.include_router(portfolios)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
