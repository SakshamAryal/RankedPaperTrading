from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies.db_dependency import get_db
from app.dependencies.user_dependency import get_current_user
from app.schemas.user import UserCreate, UserResponse
from app.utils.password import hash_password
from app.models.user import User

users = APIRouter(
    prefix="/users",
    tags=["users"],
)


@users.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.password.get_secret_value()),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

@users.get("/me", response_model=UserResponse)
async def user_info(user: User =  Depends(get_current_user)):
    return user
