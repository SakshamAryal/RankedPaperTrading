from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
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


@users.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=409, detail="Username already taken.")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="Email already registered.")
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.password.get_secret_value()),
    )
    db.add(new_user)
    # the checks above can race with another signup; the unique constraints have the final say
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username or email already taken.")
    db.refresh(new_user)
    return new_user

@users.get("/me", response_model=UserResponse)
def user_info(user: User =  Depends(get_current_user)):
    return user
