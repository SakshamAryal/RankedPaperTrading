from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException, Body
from jose import JWTError, ExpiredSignatureError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from app.schemas.token import Token
from app.utils.password import authenticate_user
from app.utils.jwt import create_access_token, create_refresh_token, decode_token, revoke_refresh_token
from app.config import settings
from app.dependencies.db_dependency import get_db
from app.models.user import User
from app.models.refresh_token import RefreshToken

auth = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@auth.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    user_id = user.id
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {"sub": str(user_id)},
        access_token_expires,
    )
    refresh_token = create_refresh_token(user_id, db)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@auth.post("/refresh", response_model=Token)
def refresh_token(token: str = Body(...), db: Session = Depends(get_db)):
    try:
        # check for the correct type of token
        payload = decode_token(token)
        if "token_type" not in payload or payload["token_type"] != "refresh":
            raise HTTPException(status_code=403, detail="Invalid refresh token")

        # check if the stored refresh token has expired
        db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
        if not db_token or db_token.is_revoked:
            raise HTTPException(status_code=403, detail="Invalid refresh token")

        # validate the user with db
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=403, detail="Could not validate credentials")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User does not exist")

        # create and revoke refresh tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            {"sub": str(user.id)},
            access_token_expires,
        )
        new_refresh_token = create_refresh_token(user.id, db)
        revoke_refresh_token(token, db)
        return Token(access_token=access_token, refresh_token=new_refresh_token, token_type="bearer")

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


@auth.post("/logout")
def logout(token: str = Body(...), db: Session = Depends(get_db)):
    revoke_refresh_token(token, db)
    return {"message": "Successfully logged out"}
